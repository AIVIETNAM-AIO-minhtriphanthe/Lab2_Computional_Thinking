from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore

db = get_firestore()


def add_task(uid: str, title: str, description: str = "") -> str:
    """Thêm task mới vào Firestore, trả về ID document vừa tạo"""
    doc_ref = (
        db.collection("todos")
        .document(uid)
        .collection("tasks")
        .document()
    )
    doc_ref.set({
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    })
    return doc_ref.id


def get_tasks(uid: str) -> list:
    """Lấy tất cả tasks của user, sắp xếp từ cũ đến mới"""
    query = (
        db.collection("todos")
        .document(uid)
        .collection("tasks")
        .order_by("created_at")
    )
    docs = list(query.stream())
    return [
        {
            "id": doc.id,
            "title": doc.to_dict().get("title", ""),
            "description": doc.to_dict().get("description", ""),
            "completed": doc.to_dict().get("completed", False),
        }
        for doc in docs
    ]


def update_task_status(uid: str, task_id: str, completed: bool):
    """Cập nhật trạng thái hoàn thành của một task"""
    (
        db.collection("todos")
        .document(uid)
        .collection("tasks")
        .document(task_id)
        .update({"completed": completed})
    )


def delete_task(uid: str, task_id: str):
    """Xoá một task khỏi Firestore"""
    (
        db.collection("todos")
        .document(uid)
        .collection("tasks")
        .document(task_id)
        .delete()
    )
