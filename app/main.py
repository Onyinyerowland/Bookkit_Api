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

def create_app() -> FastAPI:
    app = FastAPI(
        title="Bookkit API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    @app.get("/", tags=["home"])
    async def read_root():
        return {
            "message": "Welcome to BookIt API 🎉",
            "docs": "/docs",
            "redoc": "/redoc",
            "version": "1.0.0"
        }

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
app = create_app()

for route in app.routes:
    print(route.path)
