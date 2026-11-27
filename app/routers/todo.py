from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse
from app.services.todo_service import TodoService, InvalidTitleError


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