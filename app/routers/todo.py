from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_session
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoResponse
from app.services.todo_service import TodoService


router = APIRouter(prefix="/todos", tags=["todos"])


def get_service(session: Session = Depends(get_session)) -> TodoService:
    return TodoService(TodoRepository(session))


@router.get("", response_model=list[TodoResponse])
def list_todos(service: TodoService = Depends(get_service)):
    return service.list_todos()