"""
Main FastAPI application entry point.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import MonitoringMiddleware
from app.api.routers import people, planets, ai_insights, monitoring
from app.health import get_health_status
from app.db.init_db import init_db

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add monitoring middleware
app.add_middleware(MonitoringMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        logger.info(f"Connecting to database: {settings.database_url}")
        init_db()
        logger.info("Database initialization completed successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.error("Application will start without database functionality.")
        # Don't raise the exception to allow the app to start


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": f"{settings.API_V1_STR}/docs",
    }


@app.get("/health")
async def health_check():
    """Get health status for all services."""
    health_status = await get_health_status(
        settings.PROJECT_NAME, settings.APP_VERSION, settings.STAR_WARS_API_URL
    )
    return health_status


# Include API routers
app.include_router(people.router, prefix=settings.API_V1_STR)
app.include_router(planets.router, prefix=settings.API_V1_STR)
app.include_router(ai_insights.router, prefix=settings.API_V1_STR)
app.include_router(monitoring.router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
