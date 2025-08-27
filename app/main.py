import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from Database.db import db
from app.config.settings import settings
from app.routes.auth import router as auth_router

# Configure logger
logger = logging.getLogger("uvicorn.error")  # Use uvicorn's logger
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        logger.info("Server is running and DB is connected")
    except Exception as e:
        logger.error(f"Failed to connect to the DB: {e}")
    try:
        yield
    finally:
        try:
            await db.disconnect()
            logger.info("⚠️ DB disconnected")
        except Exception as e:
            logger.error(f"Failed to disconnect DB cleanly: {e}")


app = FastAPI(
    title="Open Source Finder API",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}
