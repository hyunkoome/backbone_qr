import torch
import argparse
from pathlib import Path

def convert_checkpoint(input_path):
    input_path = Path(input_path)
    assert input_path.exists(), f"Checkpoint file not found: {input_path}"

    print(f"Loading checkpoint from: {input_path}")
    ckpt = torch.load(input_path, weights_only=False)

    # 기본적으로 'state_dict' 키 안에 weight가 있는 구조
    if 'state_dict' not in ckpt:
        raise KeyError("Expected 'state_dict' key in checkpoint, but not found.")

    output_path = input_path.parent / (input_path.stem + "_weights_only.pth")

    print(f"Saving weights-only checkpoint to: {output_path}")
    torch.save(ckpt['state_dict'], output_path)
    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .pth.tar checkpoint to weights-only .pth")
    parser.add_argument("--input_path", type=str, required=True, help="Path to .pth.tar checkpoint file")

    args = parser.parse_args()
    convert_checkpoint(args.input_path)
