import pytest

from app.models.todo import Todo
from app.services.todo_service import InvalidTitleError, TodoNotFoundError, TodoService


class FakeRepository:
    def __init__(self):
        self.items: dict[int, Todo] = {}

    def find_all(self):
        return sorted(self.items.values(), key=lambda t: t.id, reverse=True)

    def find_by_id(self, todo_id):
        return self.items.get(todo_id)

    def save(self, todo):
        if todo.id is None:
            todo.id = len(self.items) + 1
        self.items[todo.id] = todo
        return todo

    def delete(self, todo):
        del self.items[todo.id]


@pytest.fixture()
def service():
    return TodoService(FakeRepository())


def test_create_strips_title(service):
    assert service.create_todo("  공부하기 ").title == "공부하기"


def test_create_blank_title_raises(service):
    with pytest.raises(InvalidTitleError):
        service.create_todo("   ")


def test_update_missing_raises(service):
    with pytest.raises(TodoNotFoundError):
        service.update_todo(99, completed=True)


def test_update_only_completed_keeps_title(service):
    todo = service.create_todo("공부하기")
    updated = service.update_todo(todo.id, completed=True)
    assert updated.completed is True
    assert updated.title == "공부하기"


def test_delete_missing_raises(service):
    with pytest.raises(TodoNotFoundError):
        service.delete_todo(99)