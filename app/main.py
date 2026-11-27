from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, init_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
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


def to_dict(todo: Todo) -> dict:
    return {
        "id": todo.id,
        "title": todo.title,
        "completed": todo.completed,
        "created_at": todo.created_at,
    }


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@app.get("/")
def health():
    return {
        "status": "ok",
        "version": settings.version,
    }


@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate):
    title = body.title.strip()

    if not title:
        raise HTTPException(status_code=400, detail="제목을 입력하세요")

    with Session(engine) as session:
        todo = Todo(
            title=title,
            completed=False,
            created_at=now(),
        )

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return to_dict(todo)


@app.patch("/todos/{todo_id}")
def update_todo(todo_id: int, body: TodoUpdate):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")

        if body.title is not None:
            title = body.title.strip()

            if not title:
                raise HTTPException(status_code=400, detail="제목을 입력하세요")

            todo.title = title

        if body.completed is not None:
            todo.completed = body.completed

        session.commit()
        session.refresh(todo)

        return to_dict(todo)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)

        if todo is None:
            raise HTTPException(
                status_code=404,
                detail="TODO를 찾을 수 없습니다",
            )

        session.delete(todo)
        session.commit()