from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/info")
def info() -> dict[str, str]:
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "model": settings.openai_model,
        "openai_configured": "true" if settings.openai_api_key else "false",
    }
