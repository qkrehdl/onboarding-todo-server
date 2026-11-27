from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from app.models import todo

    Base.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session