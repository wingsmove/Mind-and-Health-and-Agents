"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import schemas
from app.api.routes import router
from app.core.config import get_settings
from app.services.agent import run_message_agent, run_report_agent


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # All business endpoints are mounted under the /api prefix,
    # matching the frontend proxy convention.
    app.include_router(router, prefix="/api")

    @app.post("/analyze", response_model=schemas.AnalyzeResponse)
    async def analyze(request: schemas.AnalyzeRequest) -> schemas.AnalyzeResponse:
        content = await run_message_agent(request.message)
        report = await run_report_agent(request.message, content)
        return schemas.AnalyzeResponse(content=content, report=report)

    return app


app = create_app()
