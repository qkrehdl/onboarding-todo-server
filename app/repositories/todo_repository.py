from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo import Todo


class TodoRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all(self):
        return self.session.scalars(
            select(Todo).order_by(Todo.id.desc())
        ).all()

    def save(self, todo: Todo):
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo