from fastapi import APIRouter, Depends, HTTPException

from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.tasks import CreateTaskRequest, UpdateTaskRequest
from backend.app.services.firestore_service import (
    add_task,
    get_tasks,
    update_task_status,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("")
def create_task(payload: CreateTaskRequest, user=Depends(get_current_user)):
    """Tạo task mới cho user đang đăng nhập"""
    try:
        task_id = add_task(user["uid"], payload.title, payload.description)
        return {"id": task_id, "message": "Tạo task thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def list_tasks(user=Depends(get_current_user)):
    """Lấy danh sách tất cả tasks của user"""
    try:
        tasks = get_tasks(user["uid"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{task_id}")
def update_task(task_id: str, payload: UpdateTaskRequest, user=Depends(get_current_user)):
    """Cập nhật trạng thái hoàn thành của task"""
    try:
        update_task_status(user["uid"], task_id, payload.completed)
        return {"message": "Cập nhật thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
def remove_task(task_id: str, user=Depends(get_current_user)):
    """Xoá task khỏi Firestore"""
    try:
        delete_task(user["uid"], task_id)
        return {"message": "Đã xoá task"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
