from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailRequest(BaseModel):
    item_id: int
    email_to: EmailStr
    include_image: bool = False

class TextResponse(BaseModel):
    id: int
    extracted_text: str
    error: Optional[str] = None

class AvailableIdsResponse(BaseModel):
    available_ids: list[int]

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str

class EmailSendResponse(BaseModel):
    message: str
    item_id: int
    email_to: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None