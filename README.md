# 🛍️ AI Image Retrieval BTL - Hệ thống tìm kiếm ảnh thời trang

> Có thể thêm banner minh họa vào `docs/banner.png` nếu muốn README nhìn nổi bật hơn trên GitHub.

**AI Image Retrieval BTL** là hệ thống demo tìm kiếm ảnh sản phẩm thời trang tương tự bằng Deep Learning. Người dùng chỉ cần upload một ảnh truy vấn, hệ thống sẽ trích xuất đặc trưng ảnh bằng mô hình **ResNet50 pre-trained**, so sánh với tập vector ảnh đã được index, sau đó trả về danh sách sản phẩm có độ tương đồng cao nhất.

Project được xây dựng cho bài tập lớn môn **Trí tuệ nhân tạo**, tập trung vào bài toán **Content-Based Image Retrieval (CBIR)** trên bộ dữ liệu thời trang [Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small) từ Kaggle. Theo mô tả Kaggle, dataset này gồm khoảng 44.000 sản phẩm kèm ảnh và nhãn danh mục sản phẩm.

---

## ✨ Tính năng chính

* **🔍 Tìm kiếm ảnh bằng AI**: Upload một ảnh sản phẩm, hệ thống dùng **ResNet50** để trích xuất vector đặc trưng 2048 chiều và tìm các ảnh có đặc trưng thị giác gần giống nhất.
* **🧠 Tính độ tương đồng bằng Cosine Similarity**: Vector ảnh được normalize, sau đó tính similarity bằng dot product để xếp hạng kết quả.
* **🖼️ Hiển thị kết quả trực quan**: Frontend demo hiển thị ảnh, tên sản phẩm, metadata, rank và điểm tương đồng.
* **⚙️ FastAPI Backend**: Cung cấp API upload ảnh, kiểm tra trạng thái index và trả kết quả tìm kiếm.
* **📦 Index offline**: Dataset được xử lý trước, embedding được lưu thành file `.npy` để tăng tốc truy vấn.
* **🪟 Script chạy nhanh trên Windows**: Có sẵn `.bat` để build index, chạy backend và chạy frontend tĩnh.

---

## 🏗️ Kiến trúc kỹ thuật & công nghệ

Project được thiết kế theo hướng đơn giản, dễ demo và dễ giải thích trong báo cáo: frontend demo, backend API, module AI trích xuất đặc trưng và lớp lưu trữ vector bằng file cục bộ.

### 🎨 Frontend

* **Công nghệ**: HTML, CSS, JavaScript
* **File chính**: `frontend/index.html`
* **Chức năng**:
  * Upload hoặc kéo-thả ảnh truy vấn
  * Preview ảnh query
  * Chọn số lượng kết quả `top_k`
  * Kiểm tra trạng thái backend
  * Gọi API search
  * Hiển thị lưới kết quả ảnh tương tự

### ⚙️ Backend

* **Framework**: FastAPI
* **Server**: Uvicorn
* **Ngôn ngữ**: Python
* **API chính**:
  * `GET /`
  * `GET /api/health`
  * `POST /api/search`
* **AI Model**: PyTorch + Torchvision ResNet50 pre-trained

### 🗄️ Lưu trữ dữ liệu & vector

Project hiện tại **không dùng vector database chuyên dụng** như FAISS, Milvus hoặc Pinecone. Thay vào đó, hệ thống lưu dữ liệu cục bộ:

* `data/images/`: ảnh sản phẩm
* `data/styles.csv`: metadata sản phẩm
* `data/index/embeddings.npy`: vector embedding đã trích xuất
* `data/index/ids.npy`: danh sách ID ảnh
* `data/index/metadata.json`: metadata đã chuyển sang JSON

Thông tin index hiện tại:

* Số ảnh `.jpg`: **44.442**
* Số vector đã index: **44.419**
* Kích thước mỗi vector: **2048 chiều**
* Shape embedding: **`(44419, 2048)`**

---

## 📁 Cấu trúc project

```text
btl_ai/
├── backend/
│   ├── __init__.py
│   ├── config.py              # Cấu hình đường dẫn dữ liệu và tham số mặc định
│   ├── feature_extractor.py   # Trích xuất vector đặc trưng bằng ResNet50
│   ├── build_index.py         # Tạo embedding index từ dataset
│   ├── search_engine.py       # Load index và tìm kiếm bằng cosine similarity
│   └── main.py                # FastAPI app, API search và serve frontend
├── data/
│   ├── images/                # Ảnh sản phẩm dạng {id}.jpg
│   ├── styles.csv             # Metadata sản phẩm
│   └── index/
│       ├── embeddings.npy     # Vector đặc trưng
│       ├── ids.npy            # ID ảnh tương ứng với embedding
│       └── metadata.json      # Metadata đã xử lý
├── frontend/
│   └── index.html             # Frontend demo
|
├── build_index.bat            # Script build index trên Windows
├── run_backend.bat            # Script chạy backend + frontend qua FastAPI
├── run_frontend.bat           # Script chạy frontend tĩnh riêng
├── requirements.txt
└── README.md
```

---

## 🚀 Hướng dẫn cài đặt và chạy project

### Yêu cầu hệ thống

Trước khi chạy project, cần có:

1. Python 3.9 trở lên.
2. Bộ dữ liệu [Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small).
3. File `requirements.txt` trong project.
4. Windows terminal hoặc PowerShell nếu dùng các file `.bat`.


---

## 📦 Chuẩn bị dataset

Dataset sử dụng trong project là:

**Fashion Product Images (Small)**  
Nguồn: [Kaggle - paramaggarwal/fashion-product-images-small](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)

Sau khi tải dataset từ Kaggle:

1. Giải nén file tải về.
2. Đưa thư mục `images` vào:

   ```text
   data/images/
   ```

3. Đưa file `styles.csv` vào:

   ```text
   data/styles.csv
   ```

Cấu trúc đúng:

```text
data/
├── images/
│   ├── 10000.jpg
│   ├── 10001.jpg
│   └── ...
└── styles.csv
```

File `styles.csv` gồm các cột:

```text
id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName
```

---

## 🧱 Build index

Trước khi tìm kiếm ảnh, cần tạo vector index cho dataset.

### Cách 1: Dùng script Windows

```powershell
.\build_index.bat
```

Script này sẽ:

* Tạo hoặc dùng lại môi trường ảo `.venv`
* Cài dependencies từ `requirements.txt`
* Đọc `data/styles.csv`
* Duyệt ảnh trong `data/images`
* Trích xuất embedding bằng ResNet50
* Lưu index vào `data/index`

### Cách 2: Chạy thủ công

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m backend.build_index
```

Build nhanh với số lượng ảnh giới hạn:

```powershell
python -m backend.build_index --limit 500
```

> Quá trình build index có thể mất nhiều thời gian vì hệ thống phải chạy mô hình Deep Learning trên hàng chục nghìn ảnh.

---

## ▶️ Chạy ứng dụng

### Cách nhanh nhất

Chạy backend:

```powershell
.\run_backend.bat
```

Sau đó mở trình duyệt:

```text
http://127.0.0.1:8000/
```

Route `/` của FastAPI sẽ trả về frontend demo trong `frontend/index.html`.

### Chạy frontend riêng

Nếu muốn chạy frontend tĩnh ở port `5173`:

```powershell
.\run_frontend.bat
```

Sau đó mở:

```text
http://127.0.0.1:5173/
```

Khi chạy cách này, backend vẫn cần chạy ở:

```text
http://127.0.0.1:8000
```

---

## 🔌 API

### `GET /`

Trả về giao diện frontend demo.

### `GET /api/health`

Kiểm tra backend và trạng thái index.

Response mẫu:

```json
{
  "status": "ok",
  "index_ready": true
}
```

### `POST /api/search?top_k=10`

Upload ảnh query và trả về top K ảnh tương tự.

Input:

* `file`: ảnh upload dạng multipart form-data
* `top_k`: số kết quả trả về, từ 1 đến 50

Ví dụ test bằng `curl`:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/search?top_k=3" -F "file=@data/images/10000.jpg"
```

Response mẫu:

```json
{
  "results": [
    {
      "name": "Palm Tree Girls Sp Jace Sko White Skirts",
      "gender": "Women",
      "master_category": "Apparel",
      "sub_category": "Bottomwear",
      "article_type": "Skirts",
      "base_colour": "White",
      "season": "Summer",
      "usage": "Casual",
      "id": "10000",
      "rank": 1,
      "score": 1.0,
      "image_url": "/static/images/10000.jpg"
    }
  ]
}
```

---

## 🧠 Quy trình xử lý AI

### 1. Giai đoạn tạo index offline

1. Đọc metadata từ `data/styles.csv`.
2. Lấy `id` sản phẩm.
3. Tìm ảnh tương ứng trong `data/images/{id}.jpg`.
4. Tiền xử lý ảnh theo chuẩn ResNet50:
   * Resize 256
   * CenterCrop 224
   * Chuyển sang Tensor
   * Normalize theo ImageNet mean/std
5. Trích xuất vector đặc trưng bằng ResNet50.
6. Bỏ lớp Fully Connected cuối, lấy vector 2048 chiều.
7. Normalize vector bằng L2 norm.
8. Lưu `embeddings.npy`, `ids.npy` và `metadata.json`.

### 2. Giai đoạn truy vấn online

1. Người dùng upload ảnh query.
2. Backend lưu ảnh upload vào file tạm.
3. Trích xuất vector query bằng ResNet50.
4. Tính cosine similarity giữa vector query và toàn bộ vector đã index.
5. Sắp xếp kết quả theo score giảm dần.
6. Trả về top K kết quả cho frontend.

Công thức cosine similarity:

```text
cosine(A, B) = (A . B) / (||A|| * ||B||)
```

Vì các vector đã được normalize, hệ thống có thể tính nhanh bằng dot product:

```text
scores = embeddings @ query
```

---

## 🧪 Kết quả thử nghiệm mẫu

Khi test với ảnh:

```text
data/images/10000.jpg
```

Kết quả top 1 trả về chính ảnh `10000.jpg` với score `1.0`. Điều này hợp lý vì ảnh query nằm trong dataset.

Một số kết quả tiếp theo có độ tương đồng cao về màu sắc, kiểu dáng hoặc danh mục sản phẩm. Tuy nhiên, do mô hình ResNet50 hiện tại chưa được fine-tune riêng cho dữ liệu thời trang, kết quả không phải lúc nào cũng trùng chính xác `articleType`.

---

## ⚙️ Điều chỉnh số lượng kết quả

Frontend có slider để chọn số lượng kết quả trả về.

Ở API, có thể chỉnh bằng query parameter:

```text
/api/search?top_k=10
```

Giới hạn hiện tại:

```text
1 <= top_k <= 50
```

Giá trị mặc định nằm trong `backend/config.py`:

```python
TOP_K_DEFAULT = 10
```

---

## ⚠️ Hạn chế hiện tại

* Chưa fine-tune ResNet50 trên dataset thời trang.
* Chưa dùng vector database hoặc thư viện approximate nearest neighbor như FAISS.
* Vector hiện được lưu bằng file `.npy`.
* Chưa có metric đánh giá định lượng như Precision@K, Recall@K hoặc mAP.
* Frontend mới ở mức demo/prototype.
* Chưa có đăng nhập, phân quyền, giỏ hàng hoặc dashboard quản lý sản phẩm.
* Chưa có cơ chế upload thêm sản phẩm mới từ giao diện.

---

## 🚧 Hướng phát triển

* Fine-tune model trên dataset thời trang.
* Thử nghiệm các mô hình mạnh hơn như CLIP, EfficientNet hoặc Vision Transformer.
* Tích hợp FAISS để tăng tốc tìm kiếm trên dataset lớn.
* Kết hợp đặc trưng ảnh với metadata/text embedding.
* Bổ sung metric đánh giá như Precision@K, Recall@K và mAP.
* Cải thiện frontend: filter, lịch sử tìm kiếm, loading state, responsive UI.
* Đóng gói bằng Docker để dễ triển khai.

---

## 🤝 Đóng góp

Project được xây dựng phục vụ học tập và báo cáo bài tập lớn. Có thể mở rộng theo các hướng:

1. Fork project.
2. Tạo branch mới:

   ```bash
   git checkout -b feature/ten-tinh-nang
   ```

3. Commit thay đổi:

   ```bash
   git commit -m "feat: add new feature"
   ```

4. Push branch:

   ```bash
   git push origin feature/ten-tinh-nang
   ```

5. Tạo Pull Request.

---

## 📚 Nguồn dữ liệu

* Kaggle Dataset: [Fashion Product Images (Small)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)
* Tác giả dataset: Param Aggarwal
* License dataset trên Kaggle: MIT

---

> Built for AI coursework - Image Retrieval with ResNet50 and FastAPI.
