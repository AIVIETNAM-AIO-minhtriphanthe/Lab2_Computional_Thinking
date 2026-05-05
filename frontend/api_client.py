import requests

API_BASE = "http://localhost:8000"


def _headers(id_token: str) -> dict:
    """Tạo header Authorization cho mỗi request"""
    return {"Authorization": f"Bearer {id_token}"}


# ── Auth ──────────────────────────────────────────────────────────

def signup(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/signup", json={
        "email": email,
        "password": password,
    })
    r.raise_for_status()
    return r.json()


def login(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={
        "email": email,
        "password": password,
    })
    r.raise_for_status()
    return r.json()


# ── Tasks ─────────────────────────────────────────────────────────

def get_tasks(id_token: str):
    r = requests.get(f"{API_BASE}/tasks", headers=_headers(id_token))
    r.raise_for_status()
    return r.json()


def create_task(id_token: str, title: str, description: str = ""):
    r = requests.post(
        f"{API_BASE}/tasks",
        json={"title": title, "description": description},
        headers=_headers(id_token),
    )
    r.raise_for_status()
    return r.json()


def update_task(id_token: str, task_id: str, completed: bool):
    r = requests.patch(
        f"{API_BASE}/tasks/{task_id}",
        json={"completed": completed},
        headers=_headers(id_token),
    )
    r.raise_for_status()
    return r.json()


def delete_task(id_token: str, task_id: str):
    r = requests.delete(
        f"{API_BASE}/tasks/{task_id}",
        headers=_headers(id_token),
    )
    r.raise_for_status()
    return r.json()
