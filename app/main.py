import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends

from .db import engine, Base
from .auth import router as auth_router
from .notes import router as notes_router
from .deps import get_current_user
from .models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Notes API", version="1.0.0", lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    dur_ms = (time.perf_counter() - start) * 1000
    print(f"{request.method} {request.url.path} -> {response.status_code} [{dur_ms:.2f}ms]")
    return response

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/auth/me")
async def me(current: User = Depends(get_current_user)):
    return {"id": current.id, "email": current.email, "created_at": str(current.created_at)}
