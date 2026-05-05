from pydantic import BaseModel
from typing import Optional


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = ""


class UpdateTaskRequest(BaseModel):
    completed: bool
