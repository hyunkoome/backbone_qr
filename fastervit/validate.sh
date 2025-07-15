#!/bin/bash
DATA_PATH="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/ImagenetQR/val"
MODEL="faster_vit_4_224"
BS=32 #128
#checkpoint='/home/hyunkoo/DATA/HDD8TB/Project/wataAI/output/train/barcode_fastvit_test1/20250713-221423-faster_vit_4_224-224/checkpoint-56.pth.tar'
checkpoint='/home/hyunkoo/DATA/HDD8TB/Project/wataAI/output/train/barcode_fastvit_test1/20250713-221423-faster_vit_4_224-224/model_best.pth.tar'
CLS=80

python fastervit/validate.py --num-classes ${CLS} --model ${MODEL} --checkpoint=$checkpoint --data-dir=$DATA_PATH --batch-size $BS --input-size 3 224 224