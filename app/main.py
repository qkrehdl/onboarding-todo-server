from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, init_db
from app.models.todo import Todo
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


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

        session.delete(todo)
        session.commit()