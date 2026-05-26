from pathlib import Path
'''
File cấu hình chung cho bài

Chứa các đường dẫn dữ liệu, file index và một số tham số mặc định
dùng trong hệ thống tìm kiếm ảnh
'''
BASE_DIR = Path(__file__).resolve().parent.parent           #thư mục gốc của bài 
DATA_DIR = BASE_DIR / "data"                                #thư mục chứa dữ liệu      
IMAGE_DIR = DATA_DIR / "images"                             #thư mục chứa ảnh datasets
STYLES_CSV = DATA_DIR / "styles.csv"                        #file metadata của datasets
INDEX_DIR = DATA_DIR / "index"                              #thư mục chứa vector index
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"              #flie chứa embedding vector
IDS_FILE = INDEX_DIR / "ids.npy"                            #file chứa id ảnh
METADATA_FILE = INDEX_DIR / "metadata.json"                 #file metadata json

#top kết quả tìm kiếm mặc định
TOP_K_DEFAULT = 10
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}