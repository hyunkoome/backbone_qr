import os
import shutil
from pathlib import Path
import argparse

def convert_dataset(src_root, dst_root):
    src_root = Path(src_root)
    dst_root = Path(dst_root)
    num_files = 0
    skipped = 0

    for version_dir in src_root.glob("version_*"):
        version = version_dir.name  # e.g., version_1

        for ec_dir in version_dir.iterdir():
            if not ec_dir.is_dir():
                continue
            ec = ec_dir.name  # e.g., ec_H

            for img_path in ec_dir.glob("*.png"):
                fname = img_path.stem  # e.g., v001_ecH_c001_rd_493x493
                parts = fname.split("_")

                if len(parts) < 5:
                    print(f"[SKIP] Unmatched filename: {img_path.name}")
                    skipped += 1
                    continue

                style = parts[-2]  # rd or sq
                class_name = f"{version}_{ec}_{style}"

                class_dir = dst_root / class_name
                class_dir.mkdir(parents=True, exist_ok=True)

                shutil.copy(img_path, class_dir / img_path.name)
                num_files += 1

    print(f"\n✅ Conversion completed.")
    print(f"→ Total files copied: {num_files}")
    print(f"→ Skipped (unmatched): {skipped}")
    print(f"→ Output directory: {dst_root}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert barcode dataset to ImageNet-style format.")
    parser.add_argument("--src", type=str, required=True, help="Source root directory (e.g., QR_v1_to_v10)")
    parser.add_argument("--dst", type=str, required=True, help="Target ImageNet-style output directory")
    args = parser.parse_args()

    convert_dataset(args.src, args.dst)

    """    
    convert_to_imagenet_style.py --src /home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/QR_v1_to_v10 --dst /home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/ImagenetQR
    """
