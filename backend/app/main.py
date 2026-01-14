from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.db.qdrant import _assert_embedding_dim, ping_qdrant


@asynccontextmanager
async def lifespan(app: FastAPI):
    ping_qdrant()
    _assert_embedding_dim()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
