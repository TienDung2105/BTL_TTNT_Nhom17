import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import IMAGE_DIR, TOP_K_DEFAULT
from backend.search_engine import SearchEngine

#Khởi tạo FastAPI
app = FastAPI(title="AI Image Retrieval", version="1.0.0")

#Cho phép frontend gọi API từ domain khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Public thư mục ảnh dataset để frontend có thể hiển thị ảnh kết quả
if IMAGE_DIR.exists():
    app.mount("/static/images", StaticFiles(directory=IMAGE_DIR), name="images")

engine = None


@app.on_event("startup")
def startup():
    """
    Load SearchEngine khi server khởi động
    """
    global engine
    try:
        engine = SearchEngine()
    except FileNotFoundError as exc:
        print(exc)
        engine = None


@app.get("/api/health")
def health():
    """
    Kiểm tra trạng thái API và index
    """
    return {"status": "ok", "index_ready": engine is not None}


@app.post("/api/search")
async def search_image(
    file: UploadFile = File(...),
    top_k: int = Query(TOP_K_DEFAULT, ge=1, le=50),
):
    """
    Nhận ảnh upload, tìm top K ảnh giống nhất và trả về kết quả.
    """
    #Nếu index chưa sẵn sàng thì không được search
    if engine is None:
        raise HTTPException(
            status_code=503,
            detail="Index is not ready. Run: python -m backend.build_index",
        )
    #Lấy đuôi file ảnh
    suffix = Path(file.filename or "").suffix.lower() or ".jpg"

    #Chỉ cho phép các định dạng ảnh dưới
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Only image files are supported.")

    #đọc nội dung upload
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    temp_path = None

    try:
        #Lưu ảnh upload vào file tạm để search
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(content)
            temp_path = temp.name
        #Gọi search engine tìm ảnh giống nhất
        results = engine.search(temp_path, top_k)

        #trả về frontend
        return {"results": results}

    finally:
        #Xoá file tạm
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
            