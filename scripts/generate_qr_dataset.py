import os
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
# from qrcode.image.styles.moduledrawers..styledpilimage import StyledPilImage
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, RoundedModuleDrawer
from PIL import Image
from typing import Literal


# QR 모드 capacity 계산 (numeric mode 기준)
def get_max_capacity_numeric(version: int, ec_level: Literal["L", "M", "Q", "H"]) -> int:
    # QR standard numeric capacities
    QR_CAPACITY_NUMERIC = {
        "L": lambda v:
        [0, 41, 77, 127, 187, 255, 322, 370, 461, 552, 652, 772, 883, 1022, 1101, 1250, 1408, 1548, 1725, 1903, 2061,
         2232, 2409, 2620, 2812, 3057, 3283, 3517, 3669, 3909, 4158, 4417, 4686, 4965, 5253, 5529, 5836, 6153, 6479,
         6743, 7089][v],
        "M": lambda v:
        [0, 34, 63, 101, 149, 202, 255, 293, 365, 432, 513, 604, 691, 796, 871, 991, 1082, 1212, 1346, 1500, 1600,
         1708, 1872, 2059, 2188, 2395, 2544, 2701, 2857, 3035, 3289, 3486, 3693, 3909, 4134, 4343, 4588, 4775, 5039,
         5313, 5596][v],
        "Q": lambda v:
        [0, 27, 48, 77, 111, 144, 178, 207, 259, 312, 364, 427, 489, 580, 621, 703, 775, 876, 948, 1063, 1159,
         1224, 1358, 1468, 1588, 1718, 1804, 1933, 2085, 2181, 2358, 2473, 2670, 2805, 2949, 3081, 3244, 3417, 3599,
         3791, 3993][v],
        "H": lambda v:
        [0, 17, 34, 58, 82, 106, 139, 154, 202, 235, 288, 331, 374, 427, 468, 530, 602, 674, 746, 813, 919,
         969, 1056, 1108, 1228, 1286, 1425, 1501, 1581, 1677, 1782, 1897, 2022, 2157, 2301, 2361, 2524, 2625, 2735,
         2927, 3057][v],
    }
    return QR_CAPACITY_NUMERIC[ec_level](version)


# QR 코드 생성 함수
def generate_qr_dataset_with_styles(output_root="qr_data", max_version=40, target_max_size=512):
    max_version = min(max(1, max_version), 40)  # 클램핑

    os.makedirs(output_root, exist_ok=True)
    output_root = os.path.join(output_root, f"QR_v1_to_v{max_version}")
    os.makedirs(output_root, exist_ok=True)

    ec_levels = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}
    styles = {"Square": SquareModuleDrawer(), "Rounded": RoundedModuleDrawer()}

    for version in range(1, max_version + 1):
        module_count = 21 + 4 * (version - 1)

        for ec_name, ec_level in ec_levels.items():
            max_classes = get_max_capacity_numeric(version, ec_name)

            save_dir = os.path.join(output_root, f"version_{version}", f"ec_{ec_name}")
            os.makedirs(save_dir, exist_ok=True)

            for class_id in range(1, max_classes + 1):
                data = str(class_id).zfill(3)
                for style_name, drawer in styles.items():
                    try:
                        for box_size in range(20, 0, -1):
                            border = 4
                            size = (module_count + 2 * border) * box_size

                            if size <= target_max_size:
                                qr = qrcode.QRCode(
                                    version=version,
                                    error_correction=ec_level,
                                    box_size=box_size,
                                    border=border,
                                    image_factory=StyledPilImage,
                                )
                                qr.add_data(data)
                                qr.make(fit=True)

                                img = qr.make_image(module_drawer=drawer).convert("RGB")

                                style_file_name = {'Square': 'sq', 'Rounded': 'rd'}.get(style_name, 'unk')
                                save_path = os.path.join(
                                    save_dir,
                                    f"v{version:03d}_ec{ec_name}_c{class_id:03d}_{style_file_name}_{size}x{size}.png"
                                )
                                img.save(save_path)
                                break
                    except Exception as e:
                        print(f"Failed: version={version}, ec={ec_name}, class={data}, style={style_name} ({e})")


if __name__ == "__main__":
    generate_qr_dataset_with_styles(output_root="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data", max_version=10, target_max_size=512)
