import torch

import os
import re
import json
import valid
from utils import utils
from utils import option
from data import dataset
from model import HTR_VT
from collections import OrderedDict
import pandas as pd


def main():

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(args.seed)

    args.save_dir = os.path.join(args.out_dir, args.exp_name)
    os.makedirs(args.save_dir, exist_ok=True)
    logger = utils.get_logger(args.save_dir)
    logger.info(json.dumps(vars(args), indent=4, sort_keys=True))

    model = HTR_VT.create_model(nb_cls=args.nb_cls, img_size=args.img_size[::-1])

    pth_path = args.save_dir + '/best_CER.pth'
    logger.info('loading HWR checkpoint from {}'.format(pth_path))

    ckpt = torch.load(pth_path, map_location='cpu')
    model_dict = OrderedDict()
    pattern = re.compile('module.')

    for k, v in ckpt['state_dict_ema'].items():
        if re.search("module", k):
            model_dict[re.sub(pattern, '', k)] = v
        else:
            model_dict[k] = v

    model.load_state_dict(model_dict, strict=True)
    model = model.cuda()

    logger.info('Loading test loader...')
    train_dataset = dataset.myLoadDS(args.train_data_list, args.train_data_path, args.img_size)

    test_dataset = dataset.myLoadDS(args.test_data_list, args.test_data_path, args.img_size, ralph=train_dataset.ralph, filter_charset=list(train_dataset.ralph.values()))
    test_loader = torch.utils.data.DataLoader(test_dataset,
                                              batch_size=args.val_bs,
                                              shuffle=False,
                                              pin_memory=True,
                                              num_workers=args.num_workers)

    if args.subcommand == "GERMAN":
        charset = list(
            " !#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}°´ÄÖÜßäéöü–€\"")
        converter = utils.CTCLabelConverter(charset)
    else:
        converter = utils.CTCLabelConverter(train_dataset.ralph.values())


    criterion = torch.nn.CTCLoss(reduction='none', zero_infinity=True).to(device)

    model.eval()
    with torch.no_grad():
        val_loss, val_cer, val_wer, preds, labels = valid.validation(model,
                                                                     criterion,
                                                                     test_loader,
                                                                     converter)

    logger.info(
        f'Test. loss : {val_loss:0.3f} \t CER : {val_cer:0.4f} \t WER : {val_wer:0.4f} ')

    # Erstelle eine Tabelle aus Predictions und Ground Truth
    results = pd.DataFrame({
        "prediction": preds,
        "ground_truth": labels
    })

    # Optional: falls du auch die Dateinamen speichern willst
    if hasattr(test_dataset, "samples"):
        results["filename"] = [os.path.basename(x[0]) for x in test_dataset.samples]

    # Speichern
    results.to_csv(os.path.join(args.save_dir, "predictions_vs_groundtruth.csv"), index=False)
    logger.info("Saved predictions to predictions_vs_groundtruth.csv")

if __name__ == '__main__':
    args = option.get_args_parser()
    main()

