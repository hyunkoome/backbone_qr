import torch
import argparse
from pathlib import Path
from collections import OrderedDict
import torch.serialization

# 👉 허용할 사용자 정의 타입 추가
torch.serialization.add_safe_globals([argparse.Namespace])


# def load_pretrained_ignoring_head(model, ckpt_path, verbose=True):
#     """
#     Load pretrained weights into model, excluding classification head.
#     """
#     checkpoint = torch.load(ckpt_path, map_location='cpu', weights_only=False)
#
#     if 'state_dict' in checkpoint:
#         checkpoint = checkpoint['state_dict']
#
#     filtered_ckpt = OrderedDict()
#     for k, v in checkpoint.items():
#         # if not k.startswith("head."):
#         if not k.startswith(
#                 "head.") and "relative_position" not in k and "relative_bias" not in k and "pos_embed" not in k:
#             filtered_ckpt[k] = v
#
#     missing_keys, unexpected_keys = model.load_state_dict(filtered_ckpt, strict=False)
#
#     if verbose:
#         print(f"✅ Loaded pretrained weights from {ckpt_path}")
#         print(f"🧹 Skipped head.* parameters")
#         print(f"🔑 Missing keys: {missing_keys}")
#         print(f"🧩 Unexpected keys: {unexpected_keys}")


def load_pretrained_ignoring_head(model, ckpt_path):
    checkpoint = torch.load(ckpt_path, map_location='cpu')
    state_dict = checkpoint.get("state_dict", checkpoint)

    filtered_ckpt = {}
    model_keys = dict(model.state_dict())
    for k, v in state_dict.items():
        if k in model_keys and v.shape == model_keys[k].shape:
            filtered_ckpt[k] = v
        else:
            print(f"Skipping: {k}, ckpt: {v.shape}, model: {model_keys.get(k, 'N/A')}")

    missing_keys, unexpected_keys = model.load_state_dict(filtered_ckpt, strict=False)
    print(f"Missing keys: {missing_keys}")
    print(f"Unexpected keys: {unexpected_keys}")
