#!/bin/bash

# 경로 및 하이퍼파라미터 설정
DATA_PATH="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/ImagenetQR"
MODEL="faster_vit_4_224"
BS=32
EXP="barcode_fastvit_test1"
LR=0.005
WD=0.01
WR_LR=1e-6
DR=0.1
MESA=0.05
INIT_CKPT="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/weights/fastervit_4_21k_224_w14.pth.tar"
CLS=80
CONFIG_FILE="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/fastervit/configs/faster_vit_4_224_qr.yaml"

# 학습 실행
torchrun --nproc_per_node=1 fastervit/train.py \
--config ${CONFIG_FILE} \
--mesa ${MESA} \
--num-classes ${CLS} \
--input-size 3 224 224 \
--crop-pct 0.875 \
--data_dir ${DATA_PATH} \
--model ${MODEL} \
--initial-checkpoint ${INIT_CKPT} \
--amp \
--model-ema \
--opt lamb \
--weight-decay ${WD} \
--drop-path ${DR} \
--batch-size ${BS} \
--tag ${EXP} \
--lr ${LR} \
--warmup-lr ${WR_LR}
