import torch
import torch.utils.data
import torch.backends.cudnn as cudnn
from torch.utils.tensorboard import SummaryWriter

import os
import json
import valid
from utils import utils
from utils import sam
from utils import option
from data import dataset_train
from model import HTR_VT
from functools import partial
from huggingface_hub import HfApi, HfFolder, create_repo, upload_folder

def compute_loss(args, model, image, batch_size, criterion, text, length):
    preds = model(image, args.mask_ratio, args.max_span_length, use_masking=True)
    preds = preds.float()
    preds_size = torch.IntTensor([preds.size(1)] * batch_size).cuda()
    preds = preds.permute(1, 0, 2).log_softmax(2)

    torch.backends.cudnn.enabled = False
    loss = criterion(preds, text.cuda(), preds_size, length.cuda()).mean()
    torch.backends.cudnn.enabled = True
    return loss


def main():

    args = option.get_args_parser()
    torch.manual_seed(args.seed)

    args.save_dir = os.path.join(args.out_dir, args.exp_name)
    os.makedirs(args.save_dir, exist_ok=True)

    logger = utils.get_logger(args.save_dir)
    logger.info(json.dumps(vars(args), indent=4, sort_keys=True))
    writer = SummaryWriter(args.save_dir)

    model = HTR_VT.create_model(nb_cls=args.nb_cls, img_size=args.img_size[::-1])

    total_param = sum(p.numel() for p in model.parameters())
    logger.info('total_param is {}'.format(total_param))

    model.train()
    model = model.cuda()
    model_ema = utils.ModelEma(model, args.ema_decay)
    model.zero_grad()

    logger.info('Loading train loader...')
    train_dataset = dataset_train.myLoadDS(args.train_data_list, args.data_path, args.img_size)
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=args.train_bs,
                                               shuffle=True,
                                               pin_memory=True,
                                               num_workers=args.num_workers,
                                               collate_fn=partial(dataset_train.SameTrCollate, args=args))
    train_iter = dataset_train.cycle_data(train_loader)

    logger.info('Loading val loader...')
    val_dataset = dataset_train.myLoadDS(args.val_data_list, args.data_path, args.img_size, ralph=train_dataset.ralph)
    val_loader = torch.utils.data.DataLoader(val_dataset,
                                             batch_size=args.val_bs,
                                             shuffle=False,
                                             pin_memory=True,
                                             num_workers=args.num_workers)

    optimizer = sam.SAM(model.parameters(), torch.optim.AdamW, lr=1e-7, betas=(0.9, 0.99), weight_decay=args.weight_decay)
    criterion = torch.nn.CTCLoss(reduction='none', zero_infinity=True)
    if args.subcommand in ["GERMAN"]:
        charset = list(" !#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}°´ÄÖÜßäéöü–€\"")
        converter = utils.CTCLabelConverter(charset)
    else:
        converter = utils.CTCLabelConverter(train_dataset.ralph.values())

    best_cer, best_wer = 1e+6, 1e+6
    train_loss = 0.0

    #### ---- train & eval ---- ####

    for nb_iter in range(1, args.total_iter):

        optimizer, current_lr = utils.update_lr_cos(nb_iter, args.warm_up_iter, args.total_iter, args.max_lr, optimizer)

        optimizer.zero_grad()
        batch = next(train_iter)
        image = batch[0].cuda()
        text, length = converter.encode(batch[1])
        batch_size = image.size(0)
        loss = compute_loss(args, model, image, batch_size, criterion, text, length)
        loss.backward()
        optimizer.first_step(zero_grad=True)
        compute_loss(args, model, image, batch_size, criterion, text, length).backward()
        optimizer.second_step(zero_grad=True)
        model.zero_grad()
        model_ema.update(model, num_updates=nb_iter / 2)
        train_loss += loss.item()

        if nb_iter % args.print_iter == 0:
            train_loss_avg = train_loss / args.print_iter

            logger.info(f'Iter : {nb_iter} \t LR : {current_lr:0.5f} \t training loss : {train_loss_avg:0.5f} \t ' )

            writer.add_scalar('./Train/lr', current_lr, nb_iter)
            writer.add_scalar('./Train/train_loss', train_loss_avg, nb_iter)
            train_loss = 0.0

        if nb_iter % args.eval_iter == 0:
            model.eval()
            with torch.no_grad():
                val_loss, val_cer, val_wer, preds, labels = valid.validation(model_ema.ema,
                                                                             criterion,
                                                                             val_loader,
                                                                             converter)

                if val_cer < best_cer:
                    logger.info(f'CER improved from {best_cer:.4f} to {val_cer:.4f}!!!')
                    best_cer = val_cer
                    checkpoint = {
                        'model': model.state_dict(),
                        'state_dict_ema': model_ema.ema.state_dict(),
                        'optimizer': optimizer.state_dict(),
                    }
                    torch.save(checkpoint, os.path.join(args.save_dir, 'best_CER.pth'))

                if val_wer < best_wer:
                    logger.info(f'WER improved from {best_wer:.4f} to {val_wer:.4f}!!!')
                    best_wer = val_wer
                    checkpoint = {
                        'model': model.state_dict(),
                        'state_dict_ema': model_ema.ema.state_dict(),
                        'optimizer': optimizer.state_dict(),
                    }
                    torch.save(checkpoint, os.path.join(args.save_dir, 'best_WER.pth'))

                logger.info(
                    f'Val. loss : {val_loss:0.3f} \t CER : {val_cer:0.4f} \t WER : {val_wer:0.4f} \t ')

                writer.add_scalar('./VAL/CER', val_cer, nb_iter)
                writer.add_scalar('./VAL/WER', val_wer, nb_iter)
                writer.add_scalar('./VAL/bestCER', best_cer, nb_iter)
                writer.add_scalar('./VAL/bestWER', best_wer, nb_iter)
                writer.add_scalar('./VAL/val_loss', val_loss, nb_iter)
                model.train()

#AUTOMATED UPLOAD
                if args.subcommand == "GERMAN":
                    repo_id = "Mir0da/HTR-VT-german"
                elif args.subcommand == "IAM":
                    repo_id = "Mir0da/HTR-VT-english"
                else:
                    repo_id = None  # fallback: no Upload

                token = "xxx"       #deleted due to data safety

                if repo_id is not None and (torch.cuda.current_device() == 0 or not torch.cuda.is_available()):
                    try:
                        print(f"🔼 Uploading to HuggingFace Hub as {repo_id}...")
                        create_repo(repo_id, token=token, exist_ok=True)
                        upload_folder(
                            folder_path=args.save_dir,
                            path_in_repo=".",
                            repo_id=repo_id,
                            token=token,
                            repo_type="model",
                        )
                        print("✅ Upload complete!")
                    except Exception as e:
                        print(f"⚠️ Upload failed: {e}. Training continues.")


if __name__ == '__main__':
    main()