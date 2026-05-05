from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers.auth import router as auth_router
from backend.app.routers.tasks import router as tasks_router

app = FastAPI(title="Todo App Backend")

# Cho phép frontend (Streamlit) gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Todo App API đang chạy ✅"}


@app.get("/health")
def health():
    return {"status": "ok"}
