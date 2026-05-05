# 📝 Todo App — Lab 2

Ứng dụng quản lý công việc đơn giản xây dựng với **FastAPI** (backend), **Streamlit** (frontend) và **Firebase** (Authentication + Firestore).

## Thông tin sinh viên
Họ tên: Phan Thế Minh Trí
MSSV: 24120506

## 🎬 Video Demo

[Link video demo](https://drive.google.com/file/d/10uGywtBLw3-iyxxP7eB8wJjCHkdqvVya/view?usp=sharing)

---

## 🚀 Cài đặt môi trường

```bash
# 1. Tạo virtual environment
python -m venv venv

# 2. Kích hoạt (Windows)
venv\Scripts\activate

# 2. Kích hoạt (Mac/Linux)
source venv/bin/activate

# 3. Cài dependencies
pip install -r requirements.txt
```

---

## ⚙️ Cấu hình secrets

Tạo file `.streamlit/secrets.toml` và điền thông tin Firebase:

```toml
[firebase_client]
apiKey = "..."
authDomain = "..."
databaseURL = ""
projectId = "..."
storageBucket = "..."
messagingSenderId = "..."
appId = "..."

[firebase_admin]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

---

## ▶️ Chạy Backend

```bash
# Từ thư mục gốc của project
uvicorn backend.app.main:app --reload --port 8000
```

API docs (Swagger): http://localhost:8000/docs

---

## ▶️ Chạy Frontend

```bash
venv\Scripts\activate
# Mở terminal mới, vào thư mục frontend
cd frontend
streamlit run app.py
```

Giao diện: http://localhost:8501

---

## ✨ Tính năng

- Đăng ký / đăng nhập bằng **Firebase Authentication** (Email/Password)
- Thêm task mới với tiêu đề và mô tả
- Xem danh sách tất cả tasks
- Đánh dấu task hoàn thành / chưa hoàn thành
- Xoá task
- Dữ liệu lưu vào **Firestore**, tách biệt theo từng người dùng

---

## 📁 Cấu trúc project

```
todo-app/
├── backend/
│   └── app/
│       ├── main.py
│       ├── core/firebase_config.py
│       ├── dependencies/auth.py
│       ├── routers/auth.py
│       ├── routers/tasks.py
│       ├── schemas/auth.py
│       ├── schemas/tasks.py
│       └── services/firestore_service.py
├── frontend/
│   ├── app.py
│   └── api_client.py
├── .streamlit/secrets.toml
├── .gitignore
├── requirements.txt
└── README.md
```
