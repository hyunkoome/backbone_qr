# backbone_qr

```shell
conda create -n backbone_qr python=3.10 -y
conda activate backbone_qr

sudo apt install ghostscript
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install timm transformers datasets tokenizers qrcode[pil] pillow onnx onnxruntime albumentations scikit-learn

```

```shell
ln -s /home/hyunkoo/DATA/NAS/nfsRoot/Datasets/QR_Code/hkkim_gen_qr_code_data my_data
```

데이터 구조 
```shell
backbone_qr/
├── data/
│   └── ...
├── outputs/
│   └── checkpoints/
│       └── ... (모델 저장)
├── scripts/
│   ├── generate_qr_dataset.py
│   ├── save_csv_qr_dataset_gt_labels.py
│   └── train/
│       ├── train_qr_backbone.py          ← ★ 학습 코드
│       ├── model.py                      ← ★ 모델 정의 (멀티헤드 백본 등)
│       ├── dataset.py                    ← ★ QRDataset 클래스
│       └── utils.py                      ← ★ metrics, transforms, logger 등
├── configs/
│   └── config.yaml                       ← ★ (선택) 학습 설정
├── requirements.txt
└── README.md

```
