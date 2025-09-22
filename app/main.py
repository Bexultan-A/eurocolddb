from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.records import router as records_router
from app.api.v1.branch_flags import router as branch_flags_router

def create_app() -> FastAPI:
    setup_logging(settings.APP_DEBUG)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION
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
    app.include_router(branch_flags_router, prefix="/api/v1")

    return app

app = create_app()
