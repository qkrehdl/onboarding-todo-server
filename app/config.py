import os
from dataclasses import dataclass


def _database_url() -> str:
    url = os.environ.get("DATABASE_URL")

    if not url:
        if os.environ.get("REQUIRE_DATABASE_URL") == "1":
            raise RuntimeError("DATABASE_URL 환경변수가 없습니다 — Render의 Environment에 넣으세요")
        return "sqlite:///./todo.db"

    if url.startswith(("postgresql://", "postgres://")):
        url = "postgresql+psycopg://" + url.split("://", 1)[1]

    return url


@dataclass(frozen=True)
class Settings:
    database_url: str
    allowed_origins: list[str]
    version: str


settings = Settings(
    database_url=_database_url(),
    allowed_origins=os.environ.get(
        "ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500"
    ).split(","),
    version=os.environ.get("GIT_SHA", "dev"),
)