import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

class FeatureExtractor:
    """
    Lớp xử lý trích xuất vector đặc trưng bảng ResNet50
    """

    def __init__(self):
        """
        Khởi tạo mô hình ResNet50 và tiền xử lý ảnh
        """
        try:
            print("Initializing ResNet50...")

            #tải model 
            model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

            #bỏ lớp cuối Fully Connected
            self.model = nn.Sequential(*list(model.children())[:-1])

            #chuyển sang evaluation mode
            self.model.eval()

            #tiền xử lý ảnh
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ])
            print("ResNet50 initialized successfully.")

        except Exception as e:
            print(f"Model initialization error: {e}")
            raise e
        
    def extract_features(self, image_path):
        """
        Nhận đường dẫn ảnh và trả về vector đặc trưng đã normalize

        Args:
            image_path: Đường dẫn đến ảnh.
        Returns:
            numpy.ndarray: Vector đặc trưng hoặc None nếu lỗi.

        """

        try:
            #đọc ảnh và ép về RGB (tránh xung đột) 
            image = Image.open(image_path).convert("RGB")

            # tiền xử lý ảnh
            tensor = self.transform(image).unsqueeze(0)

            #tắt gradient để tiết kiệm bộ nhớ
            with torch.no_grad():
                #trích xuất vector đặc trưng
                vector = (
                    self.model(tensor)
                    .flatten()
                    .cpu()
                    .numpy()
                    .astype("float32")
                )

            # normalize vector để dùng cosine similarity
            norm = np.linalg.norm(vector)

            if norm > 0:
                vector = vector / norm

            return vector
        
        except FileNotFoundError:
            print(f"Image not found: {image_path}")
            return None
        
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return None
