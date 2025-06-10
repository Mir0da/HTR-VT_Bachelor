python train.py --exp-name german \
--max-lr 1e-3 \
--train-bs 64 \
--val-bs 8 \
--weight-decay 0.5 \
--mask-ratio 0.4 \
--attn-mask-ratio 0.1 \
--max-span-length 8 \
--img-size 1024 64 \
--patch-size 4 16
--proj 8 \
--dila-ero-max-kernel 2 \
--dila-ero-iter 1 \
--proba 0.5 \
--alpha 1 \
--total-iter 100000 \
--print-iter 100 \
GERMAN


python train.py --exp-name german --max-lr 1e-3 --train-bs 64 --val-bs 8 --weight-decay 0.5 --mask-ratio 0.4 --attn-mask-ratio 0.1 --max-span-length 8 --img-size 1024 64 --patch-size 4 16 --proj 8 --dila-ero-max-kernel 2 --dila-ero-iter 1 --proba 0.5 --alpha 1 --total-iter 100000 --print-iter 100 GERMAN