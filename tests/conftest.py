import os
import tempfile

_db = os.path.join(tempfile.mkdtemp(prefix="todo-test-"), "test.db")
os.environ["DATABASE_URL"] = "sqlite:///" + _db.replace("\\", "/")
os.environ.pop("REQUIRE_DATABASE_URL", None)

import pytest
from fastapi.testclient import TestClient

from app.main import app

try:
    from app.database import Base, engine
except ImportError:
    from app.main import Base, engine


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c