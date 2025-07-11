import os
import csv
import re
from collections import Counter

def generate_qr_labels_csv(data_root, output_csv="qr_labels.csv"):
    """
    QR 백본 학습용 라벨 CSV 생성
    파일명 형식: v{version}_ec{ec}_c{class_id}_{style}_{width}x{height}.png
    """

    entries = []
    version_counter = Counter()
    ec_counter = Counter()
    style_counter = Counter()
    class_ids = set()

    for root, _, files in os.walk(data_root):
        for fname in files:
            if not fname.endswith(".png"):
                continue

            match = re.match(r"v(\d+)_ec([LMQH])_c(\d+)_([a-z]+)_(\d+)x(\d+)\.png", fname)
            if not match:
                print(f"Skipped (no match): {fname}")
                continue

            version, ec, class_id, style, width, height = match.groups()
            rel_path = os.path.relpath(os.path.join(root, fname), data_root)

            version = int(version)
            class_id = int(class_id)
            width = int(width)
            height = int(height)

            entries.append({
                "version": version,
                "error_correlation": ec,
                "style": style,
                "class_id": class_id,
                "width": width,
                "height": height,
                "filepath": rel_path,
            })

            # 카운터 집계
            version_counter[version] += 1
            ec_counter[ec] += 1
            style_counter[style] += 1
            class_ids.add(class_id)

    # 정렬: version, error_correlation, style, class_id
    entries.sort(key=lambda x: (x["version"], x["error_correlation"], x["style"], x["class_id"]))

    # Write to CSV
    csv_path = os.path.join(data_root, output_csv)
    fieldnames = ["version", "error_correlation", "style", "class_id", "width", "height", "filepath"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)

    # 카테고리별 통계 출력
    print(f"\n✅ Saved CSV: {csv_path} ({len(entries)} entries)")
    print("\n📊 데이터 분포:")
    print("▶ Version 분포:", dict(sorted(version_counter.items())))
    print("▶ Error Correction 분포:", dict(sorted(ec_counter.items())))
    print("▶ Style 분포:", dict(sorted(style_counter.items())))
    print(f"▶ 고유 Class ID 개수: {len(class_ids)}\n")


if __name__ == "__main__":
    # 사용 예시
    generate_qr_labels_csv("/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/QR_v1_to_v10")
