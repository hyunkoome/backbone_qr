# backbone_qr

```shell
conda create -n backbone_qr python=3.10 -y
conda activate backbone_qr
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install timm transformers datasets tokenizers qrcode[pil] pillow onnx onnxruntime albumentations scikit-learn

```