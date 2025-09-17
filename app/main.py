from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.records import router as records_router

def create_app() -> FastAPI:
    setup_logging(settings.APP_DEBUG)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        openapi_url="/openapi.json",
        redoc_url="/redoc",
    )

    # CORS
    origins = ["*"] if settings.APP_CORS_ORIGINS == "*" else [
        o.strip() for o in settings.APP_CORS_ORIGINS.split(",") if o.strip()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # v1 routes
    app.include_router(records_router, prefix="/api/v1")

    return app

app = create_app()
