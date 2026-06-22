"""
Fin — FastAPI application entrypoint.

Run with:
    uvicorn main:app --reload --port 8000
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.database import mongo
from app.routes import (
    auth_routes, transaction_routes, goal_routes,
    reminder_routes, analytics_routes, csv_routes, ai_routes,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("fin.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongo.connect()
    logger.info(f"{settings.APP_NAME} started in '{settings.APP_ENV}' mode")
    yield
    # Shutdown
    await mongo.disconnect()
    logger.info(f"{settings.APP_NAME} shut down cleanly")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered personal finance assistant with multi-agent insights.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."},
    )


# --- Routers ---
app.include_router(auth_routes.router)
app.include_router(transaction_routes.router)
app.include_router(goal_routes.router)
app.include_router(reminder_routes.router)
app.include_router(analytics_routes.router)
app.include_router(csv_routes.router)
app.include_router(ai_routes.router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    try:
        await mongo.client.admin.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"
    return {"status": "ok", "database": db_status}
