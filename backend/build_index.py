import argparse
import json

import numpy as np
import pandas as pd
from tqdm import tqdm

from backend.config import (
    IMAGE_DIR,
    INDEX_DIR,
    IDS_FILE,
    EMBEDDINGS_FILE,
    METADATA_FILE,
    STYLES_CSV,
)
from backend.feature_extractor import FeatureExtractor


def build_metadata(row):
    """
    Lấy thông tin metadata của từng sản phẩm từ styles.csv
    """
    return {
        "name": str(row.get("productDisplayName", "")),
        "gender": str(row.get("gender", "")),
        "master_category": str(row.get("masterCategory", "")),
        "sub_category": str(row.get("subCategory", "")),
        "article_type": str(row.get("articleType", "")),
        "base_colour": str(row.get("baseColour", "")),
        "season": str(row.get("season", "")),
        "usage": str(row.get("usage", "")),
    }


def main():
    """
    Tạo index vector cho toàn bộ ảnh trong datasets
    """
    parser = argparse.ArgumentParser(description="Build local image retrieval index.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Giới hạn số ảnh để test nhanh.",
    )
    args = parser.parse_args()

    #Kiểm tra file metadata
    if not STYLES_CSV.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {STYLES_CSV}")

    #Kiểm tra thư mục ảnh
    if not IMAGE_DIR.exists():
        raise FileNotFoundError(f"Không tìm thấy thư mục: {IMAGE_DIR}")

    #Tạo thư mục index nếu chưa có
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    #Đọc file styles.csv
    df = pd.read_csv(STYLES_CSV, on_bad_lines="skip") #on_bad_lines="skip": bỏ qua dòng lỗi format

    #Nếu test nhanh thì chỉ lấy một số dòng đầu bằng --limit vd: py -m backend.build_index --limit 10
    if args.limit:
        df = df.head(args.limit)

    #Khởi tạo model trích xuất đặc trưng
    extractor = FeatureExtractor()

    ids = []
    embeddings = []
    metadata = {}

    #Duyệt toàn bộ dataset
    for _, row in tqdm(
        df.iterrows(),
        total=len(df), 
        desc="Building index"
        ):

        product_id = str(row.get("id"))

        #Ảnh trong dataset có dạng: id.jpg
        image_path = IMAGE_DIR / f"{product_id}.jpg"

        #Bỏ qua nếu ảnh không tồn tại
        if not image_path.exists():
            continue

        #Trích xuất vector bằng ResNet50
        vector = extractor.extract_features(image_path)

        #Nếu lỗi thì bỏ qua ảnh đó
        if vector is None:
            print(f"Bỏ qua {product_id}: không trích xuất được vector")
            continue

        #Lưu dữ liệu
        ids.append(product_id)
        embeddings.append(vector)
        metadata[product_id] = build_metadata(row)

    if not embeddings:
        raise RuntimeError("Không có ảnh nào được index. Kiểm tra data/images và styles.csv.")

    #Lưu embeddings, ids và metadata
    np.save(EMBEDDINGS_FILE, np.vstack(embeddings).astype("float32"))
    np.save(IDS_FILE, np.array(ids))
    METADATA_FILE.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Đã index {len(ids)} ảnh vào {INDEX_DIR}")


if __name__ == "__main__":
    main()