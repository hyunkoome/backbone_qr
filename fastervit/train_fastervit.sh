#!/bin/bash

# 데이터 경로
DATA_PATH="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/ImagenetQR"

# 모델 설정
MODEL=faster_vit_4_224
PRETRAINED_PATH="/home/hyunkoo/DATA/HDD8TB/weights/faster_vit_4_224.pth"

# 학습 하이퍼파라미터
BS=32
EXP=FT_Barcode_FasterViT4
LR=5e-4
WD=0.01
WR_LR=1e-6
DR=0.2
MESA=0.1

# 학습 실행
torchrun --nproc_per_node=1 train.py \
--data_dir=$DATA_PATH \
--model $MODEL \
--pretrained $PRETRAINED_PATH \
--amp \
--batch-size $BS \
--drop-path $DR \
--weight-decay $WD \
--lr $LR \
--warmup-lr $WR_LR \
--mesa $MESA \
--input-size 3 224 224 \
--crop-pct=0.875 \
--tag $EXP

