import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import auth, posts, users

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="Backend Production API",
    description="User authentication and posts management REST API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])


@app.get("/")
def read_root():
    return {"message": "Backend Production API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
