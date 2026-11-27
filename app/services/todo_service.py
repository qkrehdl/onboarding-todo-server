from datetime import datetime

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository


class InvalidTitleError(Exception):
    pass


class TodoNotFoundError(Exception):
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

    def update_todo(
        self,
        todo_id: int,
        title: str | None = None,
        completed: bool | None = None,
    ):
        todo = self.repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError()

        if title is not None:
            title = title.strip()

            if not title:
                raise InvalidTitleError()

            todo.title = title

        if completed is not None:
            todo.completed = completed

        return self.repository.save(todo)

    def delete_todo(self, todo_id: int):
        todo = self.repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError()

        self.repository.delete(todo)