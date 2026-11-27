from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import todo


app = FastAPI(title="onboarding-todo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(todo.router)


@app.get("/")
def health():
    return {"status": "ok", "version": settings.version}