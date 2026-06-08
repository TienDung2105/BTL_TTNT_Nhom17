import json
import numpy as np
from backend.config import (
    EMBEDDINGS_FILE,
    IDS_FILE,
    METADATA_FILE,
)

from model.feature_extractor import FeatureExtractor


class SearchEngine:
    """
    Hệ thống tìm kiếm ảnh bằng cosine similarity
    """

    def __init__(self):
        """
        Khởi tạo search engine và load index
        """
        self.extractor = FeatureExtractor()

        self.embeddings = None
        self.ids = None
        self.metadata = None

        self.load_index()

    def load_index(self):
        """
        Load embeddings, ids và metadata từ data/index
        """

        #Kiểm tra index tồn tại
        if (
            not EMBEDDINGS_FILE.exists()
            or not IDS_FILE.exists()
            or not METADATA_FILE.exists()
        ):
            raise FileNotFoundError(
                "Index not found. Run: python -m model.build_index"
            )

        #Load vector embeddings
        self.embeddings = np.load(EMBEDDINGS_FILE).astype("float32")

        #Load danh sách id ảnh
        self.ids = np.load(IDS_FILE).astype(str)

        #Load metadata json
        self.metadata = json.loads(
            METADATA_FILE.read_text(encoding="utf-8")
        )

    def search(self, image_path, top_k=10):
        """
        Tìm top K ảnh giống nhất

        Args:
            image_path: Đường dẫn ảnh query

            top_k: Số lượng kết quả trả về

        Returns:
            list: Danh sách ảnh tương tự
        """

        #Trích xuất vector query
        query = self.extractor.extract_features(image_path)

        if query is None:
            raise ValueError("Không thể trích xuất vector từ ảnh query.")

        #Cosine similarity
        #Vì vector đã normalize nên: cosine similarity = dot product
        scores = self.embeddings @ query

        #Lấy top K ảnh có score cao nhất
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for rank, idx in enumerate(top_indices, start=1):

            #Lấy id ảnh
            product_id = str(self.ids[idx])

            #Copy metadata
            item = self.metadata.get(product_id, {}).copy()

            #Thêm thông tin kết quả
            item["id"] = product_id

            item["rank"] = rank

            item["score"] = round(float(scores[idx]), 4)

            #URL ảnh cho frontend
            item["image_url"] = f"/static/images/{product_id}.jpg"

            results.append(item)

        return results
