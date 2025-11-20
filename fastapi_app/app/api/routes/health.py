from fastapi import APIRouter
from datetime import datetime
from app.domain.models import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        service="FastAPI Email Service",
        timestamp=datetime.utcnow().isoformat()
    )