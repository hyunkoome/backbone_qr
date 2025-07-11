# import os
# import qrcode
# from PIL import Image
# from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
# from multiprocessing import Pool, cpu_count
import os
import math
import qrcode
import segno
import treepoem
import multiprocessing
from PIL import Image
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


# def generate_qr_dataset(output_root: str = "../data", box_sizes: list = [6, 8, 10, 12], border: int = 4):
#
#     versions = range(1, 41)
#     error_corrections: dict = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q,
#                                "H": ERROR_CORRECT_H}
#     for version in versions:
#         for ec_name, ec_level in error_corrections.items():
#             for box_size in box_sizes:
#                 # Prepare directory
#                 dirpath = os.path.join(
#                     output_root,
#                     f"version_{version}",
#                     f"ec_{ec_name}",
#                     f"box_{box_size}"
#                 )
#                 os.makedirs(dirpath, exist_ok=True)
#
#                 # Data string identifies the combination
#                 data = f"v{version}_ec{ec_name}_box{box_size}"
#
#                 # Generate QR
#                 qr = qrcode.QRCode(
#                     version=version,
#                     error_correction=ec_level,
#                     box_size=box_size,
#                     border=border
#                 )
#                 qr.add_data(data)
#                 qr.make(fit=True)
#                 img = qr.make_image(fill_color="black", back_color="white")
#
#                 # Save image
#                 filename = os.path.join(dirpath, f"{data}.png")
#                 img.save(filename)
#                 print(f"Saved {filename}")


"""
Generates QR codes for all combinations of version, error correction level, and box size,
saving one image per combination in a structured directory under output_root.

Directory structure:
  data/
    version_<version>/
      ec_<L/M/Q/H>/
        box_<box_size>/
          v<version>_ec<level>_box<box_size>.png

QR 코드의 버전(version)
    “모듈(module)”이라 불리는 셀(cell) 한 변의 개수를 결정하는 값
    버전 1: 21×21 모듈
    버전 2: 25×25 모듈
    ...
    버전 n: (21 + 4·(n–1)) × (21 + 4·(n–1)) 모듈
    최대 버전 40: 177×177 모듈

    즉, 버전이 커질수록 한 변에 들어가는 셀 개수가 늘어나고, 그만큼 더 많은 데이터를 담을 수 있음
    버전	셀 크기 (modules)	최대 데이터 용량 (숫자) 대략
    1	21×21	            41자
    10	57×57	            약 174자
    20	101×101	            약 472자
    40	177×177	            약 4,296자

    데이터 양(숫자·문자·바이너리)에 따라 적절한 버전을 선택하고,
    box_size (픽셀 크기)와 border (여백) 설정에 따라 실제 이미지 해상도를 조절하면 됨

    예를 들어, version=5면 21 + 4·4 = 37 → 37×37 모듈짜리 QR 코드가 생성되고,
    box_size=8일 때 (37 + 2·border)×8 픽셀 크기의 이미지를 얻게 됨

error_corrections
    QR 코드의 오류 보정 수준(Error Correction Level) 을 지정하기 위한 딕셔너리
    QR 코드는 손상되거나 가려진 부분이 있어도 복원할 수 있도록 네 단계의 오류 보정 기능을 제공함

    레벨 키	상수 (qrcode.constants)	복원 가능 데이터 비율
    L	    ERROR_CORRECT_L	        7%
    M	    ERROR_CORRECT_M	        15%
    Q	    ERROR_CORRECT_Q	        25%
    H	    ERROR_CORRECT_H	        30%

    L (Low): 가장 낮은 보정 수준, 데이터 용량 ↑
    M (Medium): 기본값, 안정적인 보정 수준
    Q (Quartile): 중간 수준
    H (High): 가장 높은 보정 수준, 손상 복원력 ↑

    코드에서 이 딕셔너리를 순회하며 qrcode.QRCode(error_correction=…) 에 각각의 상수를 넘겨 줌으로써,
        원하는 보정 수준별로 QR 이미지를 생성할 수 있게 한 것

    일반적으로 가장 많이 쓰이는 오류 보정 수준은 Level M (15%) 입니다.
        Level L (7%): 완전히 깨끗한 환경에서 데이터 용량을 최대화할 때
        Level M (15%): 일상적인 인쇄·스캔 환경에서 균형 있게 사용
        Level Q (25%): 중간 정도의 오염·손상이 예상될 때
        Level H (30%): 공장·야외·라벨 등 훼손 가능성이 높을 때

    필요에 따라 위 네 가지 중 하나를 선택하면 되고, 특별한 지침이 없다면 Level M을 기본값으로 사용하면 무난합

box_size
    “한 개의 모듈(module, QR 셀)이 몇 픽셀 크기냐”를 정하는 값이어서,
    image_size = (module_count + 2·border) × box_size 식으로 최종 이미지 픽셀이 결정
    [6, 8, 10, 12] 은 예시일 뿐이고, 원하는 픽셀 해상도에 맞춰 얼마든지 조정할 수 있음

    예를 들어)
    version=1(21×21 모듈), border=4일 때
        box_size=6 → (21+8)×6 = 174px
        box_size=12 → (21+8)×12 = 348px

    만약 분류기로 224×224 입력을 쓰고 싶다면,
        목표 해상도 224를 (21 + 2·border) 로 나눠서 계산해 보면
        box_size ≈ 224 / (21 + 8) ≃ 7.7
        → 실수값이니 7 또는 8 중 하나를 선택하면 되고,
        결과 이미지를 Resize(224) 로 보정해 주면 됨

    box_size 설정 팁
    작게 (4~6)
        이미지 파일 크기 작음, 생성 빠름
        분류기가 저해상도 패턴에도 강건해야 할 때
    중간 (7~10)
        224~320px 범위로 맞추기 용이
        대부분 분류·디텍션 학습에 무난
    크게 (12~16 이상)
        모듈 경계가 깨끗하게 살아남아서 세밀한 버전 구분·패턴 분석에 유리
        이후 RandomResizedCrop 등 증강으로 스케일 강건성 확보

    원하는 최종 이미지 해상도와 모듈 개수(version) 에 따라 적절한 box_size 값을 골라 사용!!
    필요하다면 여러 값을 섞어서 생성해 두고,
    학습 시 RandomResizedCrop 으로도 스케일을 다양화하면 더욱 튼튼한 분류/디텍션 모델을 얻을 수 있음
"""

#
# def generate_qr_dataset_autobox(output_root: str = "data", target_size: int = 512):
#     """
#     Generates QR codes using the largest possible box_size such that the resulting image
#     is less than or equal to target_size x target_size. Automatically determines box_size
#     and border per version.
#     """
#     versions: range = range(1, 41)
#     error_corrections: dict = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}
#
#     for version in versions:
#         module_count = 21 + 4 * (version - 1)
#         for ec_name, ec_level in error_corrections.items():
#             # Find max box_size such that final image <= target_size
#             for border in range(4, 1, -1):  # try common border sizes, descending
#                 max_box_size = target_size // (module_count + 2 * border)
#                 if max_box_size <= 0:
#                     continue
#                 for box_size in range(max_box_size, 0, -1):
#                     # Final image size
#                     final_size = (module_count + 2 * border) * box_size
#                     if final_size <= target_size:
#                         # Valid combination found
#                         data = f"v{version}_ec{ec_name}_b{border}_bs{box_size}"
#                         qr = qrcode.QRCode(version=version, error_correction=ec_level, box_size=box_size, border=border)
#                         qr.add_data(data)
#                         qr.make(fit=True)
#                         img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
#
#                         # Save image
#                         dirpath = os.path.join(output_root, f"version_{version}", f"ec_{ec_name}")
#                         os.makedirs(dirpath, exist_ok=True)
#                         filename = os.path.join(dirpath, f"{data}_{final_size}x{final_size}.png")
#                         img.save(filename)
#                         print(f"Saved {filename}")
#                         break
#                 else:
#                     continue
#                 break
#
# def generate_qr_for_version(args):
#     """
#
#     :param args:
#     :return:
#     """
#     version, target_size, output_root = args
#     error_corrections = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}
#     module_count = 21 + 4 * (version - 1)
#
#     for ec_name, ec_level in error_corrections.items():
#         for border in range(4, 1, -1):
#             max_box_size = target_size // (module_count + 2 * border)
#             if max_box_size <= 0:
#                 continue
#             for box_size in range(max_box_size, 0, -1):
#                 final_size = (module_count + 2 * border) * box_size
#                 if final_size <= target_size:
#                     data = f"v{version}_ec{ec_name}_b{border}_bs{box_size}"
#                     qr = qrcode.QRCode(
#                         version=version, error_correction=ec_level,
#                         box_size=box_size, border=border
#                     )
#                     qr.add_data(data)
#                     qr.make(fit=True)
#                     img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
#
#                     dirpath = os.path.join(output_root, f"version_{version}", f"ec_{ec_name}")
#                     os.makedirs(dirpath, exist_ok=True)
#                     filename = os.path.join(dirpath, f"{data}_{final_size}x{final_size}.png")
#                     img.save(filename)
#                     print(f"[v{version}] Saved {filename}")
#                     break
#             else:
#                 continue
#             break
#
# def generate_qr_dataset_autobox_mp(output_root="data", target_size=512):
#     """
#
#     :param output_root:
#     :param target_size:
#     :return:
#     """
#     versions = list(range(1, 41))
#     args_list = [(v, target_size, output_root) for v in versions]
#     with Pool(processes=min(cpu_count(), len(versions))) as pool:
#         pool.map(generate_qr_for_version, args_list)
#
# if __name__ == "__main__":
#     # generate_qr_dataset_autobox(output_root='/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data')
#     generate_qr_dataset_autobox_mp(output_root='/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data/my_data')



# QR 오류 정정 레벨 매핑
EC_LEVELS = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}

# QR 코드 생성 (버전 x 오류정정 x 클래스 ID)
def generate_qr(version, ec_name, target_max_size, output_root):
    ec_level = EC_LEVELS[ec_name]
    module_count = 21 + 4 * (version - 1)

    # 간략한 최대 길이 추정 (숫자 모드 기준)
    max_len = {
        "L": 7089, "M": 5596, "Q": 3993, "H": 3057
    }[ec_name] if version == 40 else int((version * 35) * {
        "L": 1.0, "M": 0.8, "Q": 0.6, "H": 0.45
    }[ec_name])

    for class_id in range(1, max_len + 1):
        data = str(class_id).zfill(3)
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
                    )
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                    save_dir = os.path.join(output_root, "QR", f"version_{version}", f"ec_{ec_name}", f"class_{data}")
                    os.makedirs(save_dir, exist_ok=True)
                    filename = f"v{version}_ec{ec_name}_c{data}_{size}x{size}.png"
                    img.save(os.path.join(save_dir, filename))
                    break
        except Exception as e:
            print(f"[QR FAIL] v{version} ec={ec_name} class={data}: {e}")

# PDF417, DataMatrix 바코드 생성 함수
def generate_treepoem_barcode(barcode_type, output_root, max_classes=500):
    for class_id in range(1, max_classes + 1):
        data = str(class_id).zfill(3)
        try:
            barcode = treepoem.generate_barcode(barcode_type=barcode_type, data=data)
            save_dir = os.path.join(output_root, barcode_type.upper(), f"class_{data}")
            os.makedirs(save_dir, exist_ok=True)
            barcode.convert("RGB").save(os.path.join(save_dir, f"{barcode_type}_{data}.png"))
        except Exception as e:
            print(f"[{barcode_type.upper()} FAIL] class={data}: {e}")

# EAN13은 숫자 12자리 + 체크디짓 1자리 필요
def generate_ean13(output_root, max_classes=500):
    for class_id in range(1, max_classes + 1):
        base = "123" + str(class_id).zfill(9 - 3)
        try:
            barcode = treepoem.generate_barcode(barcode_type="ean13", data=base)
            save_dir = os.path.join(output_root, "EAN13", f"class_{str(class_id).zfill(3)}")
            os.makedirs(save_dir, exist_ok=True)
            barcode.convert("RGB").save(os.path.join(save_dir, f"ean13_{base}.png"))
        except Exception as e:
            print(f"[EAN13 FAIL] class={base}: {e}")

# 전체 바코드 생성 함수
def generate_all(output_root="barcode_data", target_max_size=512):
    # QR코드는 멀티프로세싱 병렬처리
    jobs = []
    for version in range(1, 41):
        for ec in ["L", "M", "Q", "H"]:
            jobs.append((version, ec, target_max_size, output_root))

    print("▶ QR 코드 생성 시작...")
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.starmap(generate_qr, jobs)

    # print("▶ PDF417 생성...")
    # generate_treepoem_barcode("pdf417", output_root)
    #
    # print("▶ DataMatrix 생성...")
    # generate_treepoem_barcode("datamatrix", output_root)
    #
    # print("▶ EAN-13 생성...")
    # generate_ean13(output_root)

# 실행
if __name__ == "__main__":
    generate_all(output_root="/home/hyunkoo/DATA/HDD8TB/Project/wataAI/backbone_qr/data", target_max_size=512)
