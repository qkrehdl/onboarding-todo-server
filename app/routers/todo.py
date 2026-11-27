from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import (
    TodoService,
    InvalidTitleError,
    TodoNotFoundError,
)


router = APIRouter(prefix="/todos", tags=["todos"])


def get_service(session: Session = Depends(get_session)) -> TodoService:
    return TodoService(TodoRepository(session))


@router.get("", response_model=list[TodoResponse])
def list_todos(service: TodoService = Depends(get_service)):
    return service.list_todos()


@router.post("", status_code=201, response_model=TodoResponse)
def create_todo(
    body: TodoCreate,
    service: TodoService = Depends(get_service),
):
    try:
        return service.create_todo(body.title)
    except InvalidTitleError:
        raise HTTPException(status_code=400, detail="제목을 입력하세요")


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    body: TodoUpdate,
    service: TodoService = Depends(get_service),
):
    try:
        return service.update_todo(
            todo_id,
            title=body.title,
            completed=body.completed,
        )
    except InvalidTitleError:
        raise HTTPException(status_code=400, detail="제목을 입력하세요")
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    service: TodoService = Depends(get_service),
):
    try:
        service.delete_todo(todo_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="TODO를 찾을 수 없습니다")