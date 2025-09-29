import sys
import asyncio

# Fix for Windows event loop policy
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.routers import auth, user, service, booking, review


def get_app() -> FastAPI:
    return app
def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="BookIt API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )


    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Logging setup
    logger.add("logs/bookit.log", rotation="10 MB", retention="7 days", level="INFO")
    logger.info("BookIt API initialized")

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(user.router, prefix="/user", tags=["user"])
    app.include_router(service.router, prefix="/service", tags=["service"])
    app.include_router(booking.router, prefix="/booking", tags=["booking"])
    app.include_router(review.router, prefix="/review", tags=["review"])

    return app


# Global app instance for ASGI servers and testing
app = create_app()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=str(settings.HOST), port=settings.PORT)
    logger.info(f"Starting server at http://{settings.HOST}:{settings.PORT}")
    logger.info("BookIt API started")
    logger.info("BookIt API shutdown")
