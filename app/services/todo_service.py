from datetime import datetime

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository


class InvalidTitleError(Exception):
    pass


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def list_todos(self):
        return self.repository.find_all()

    def create_todo(self, title: str):
        title = title.strip()

        if not title:
            raise InvalidTitleError()

        todo = Todo(
            title=title,
            completed=False,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )

        return self.repository.save(todo)