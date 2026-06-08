const els = {
    apiBase: document.querySelector("#apiBase"),
    clearBtn: document.querySelector("#clearBtn"),
    dropzone: document.querySelector("#dropzone"),
    fileInput: document.querySelector("#fileInput"),
    fileName: document.querySelector("#fileName"),
    message: document.querySelector("#message"),
    preview: document.querySelector("#preview"),
    previewImage: document.querySelector("#previewImage"),
    resultCount: document.querySelector("#resultCount"),
    results: document.querySelector("#results"),
    searchBtn: document.querySelector("#searchBtn"),
    status: document.querySelector("#status"),
    statusText: document.querySelector("#statusText"),
    topK: document.querySelector("#topK"),
    topKValue: document.querySelector("#topKValue"),
    uploadCopy: document.querySelector("#uploadCopy")
};

let selectedFile = null;
let previewUrl = null;

function apiUrl(path) {
    return `${els.apiBase.value.replace(/\/+$/, "")}${path}`;
}

function setMessage(text, isError = false) {
    els.message.textContent = text;
    els.message.classList.toggle("error", isError);
}

function setStatus(kind, text) {
    els.status.className = `status ${kind || ""}`.trim();
    els.statusText.textContent = text;
}

async function checkHealth() {
    setStatus("", "Đang kiểm tra");

    try {
        const res = await fetch(apiUrl("/api/health"));
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (data.index_ready) {
            setStatus("ready", "Sẵn sàng");
        } else {
            setStatus("error", "Chưa có index");
            setMessage("Backend chạy được nhưng index chưa sẵn sàng. Hãy chạy: python -m backend.build_index", true);
        }
    } catch (error) {
        setStatus("error", "Mất kết nối");
        setMessage("Không kết nối được backend. Hãy chạy uvicorn backend.main:app --reload.", true);
    }
}

function setFile(file) {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
        setMessage("File được chọn không phải ảnh.", true);
        return;
    }

    selectedFile = file;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = URL.createObjectURL(file);

    els.previewImage.src = previewUrl;
    els.fileName.textContent = file.name;
    els.preview.classList.add("has-image");
    els.uploadCopy.style.display = "none";
    els.searchBtn.disabled = false;
    setMessage("Ảnh đã sẵn sàng. Bấm tìm để gửi lên backend.");
}

function clearAll() {
    selectedFile = null;
    els.fileInput.value = "";
    els.searchBtn.disabled = true;
    els.preview.classList.remove("has-image");
    els.previewImage.removeAttribute("src");
    els.fileName.textContent = "";
    els.uploadCopy.style.display = "grid";
    els.resultCount.textContent = "Chưa có kết quả";
    els.results.innerHTML = '<div class="empty">Upload một ảnh sản phẩm để xem các ảnh gần giống nhất.</div>';
    setMessage("Chọn ảnh để bắt đầu.");

    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
        previewUrl = null;
    }
}

function fieldValue(item, key) {
    const value = item[key];
    if (!value || value === "nan" || value === "NaN") return "";
    return String(value);
}

function renderResults(results) {
    if (!results.length) {
        els.resultCount.textContent = "Không có kết quả";
        els.results.innerHTML = '<div class="empty">Backend không trả về ảnh phù hợp.</div>';
        return;
    }

    els.resultCount.textContent = `${results.length} kết quả`;
    els.results.innerHTML = results.map((item) => {
        const tags = [
            fieldValue(item, "gender"),
            fieldValue(item, "article_type"),
            fieldValue(item, "base_colour"),
            fieldValue(item, "usage")
        ].filter(Boolean);
        const score = Number(item.score || 0);
        const scorePercent = Math.max(0, Math.min(100, score * 100));
        const imageSrc = apiUrl(item.image_url || "");
        const title = fieldValue(item, "name") || `Ảnh ${item.id || item.rank}`;

        return `
          <article class="card">
            <img class="thumb" src="${escapeHtml(imageSrc)}" alt="${escapeHtml(title)}" loading="lazy">
            <div class="card-body">
              <div class="card-top">
                <h3 class="name">${escapeHtml(title)}</h3>
                <span class="rank">#${escapeHtml(String(item.rank || ""))}</span>
              </div>
              <div class="meta">
                ${tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
              </div>
              <div class="score">
                <span>Score ${score.toFixed(4)}</span>
                <span class="score-bar"><span class="score-fill" style="width:${scorePercent}%"></span></span>
              </div>
            </div>
          </article>
        `;
    }).join("");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function search() {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    els.searchBtn.disabled = true;
    setMessage("Đang tìm kiếm...");
    els.results.innerHTML = '<div class="empty">Đang xử lý ảnh query...</div>';

    try {
        const res = await fetch(apiUrl(`/api/search?top_k=${els.topK.value}`), {
            method: "POST",
            body: formData
        });
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || `Search lỗi HTTP ${res.status}`);
        }

        renderResults(data.results || []);
        setMessage("Hoàn tất.");
    } catch (error) {
        els.results.innerHTML = '<div class="empty">Không thể hiển thị kết quả.</div>';
        setMessage(error.message || "Có lỗi khi tìm kiếm.", true);
    } finally {
        els.searchBtn.disabled = !selectedFile;
    }
}

els.fileInput.addEventListener("change", (event) => {
    setFile(event.target.files[0]);
});

els.dropzone.addEventListener("dragover", (event) => {
    event.preventDefault();
    els.dropzone.classList.add("dragging");
});

els.dropzone.addEventListener("dragleave", () => {
    els.dropzone.classList.remove("dragging");
});

els.dropzone.addEventListener("drop", (event) => {
    event.preventDefault();
    els.dropzone.classList.remove("dragging");
    setFile(event.dataTransfer.files[0]);
});

els.topK.addEventListener("input", () => {
    els.topKValue.textContent = els.topK.value;
});

els.apiBase.addEventListener("change", checkHealth);
els.searchBtn.addEventListener("click", search);
els.clearBtn.addEventListener("click", clearAll);

checkHealth();