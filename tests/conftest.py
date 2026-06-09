import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

TEST_DB_PATH = Path(__file__).parent / "test_app.db"

if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["INITIAL_ADMIN_EMAIL"] = ""

from main import app
import routes


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def disable_emails(monkeypatch):
    monkeypatch.setattr(routes, "send_signup_email", lambda email: True)
    monkeypatch.setattr(routes, "send_login_email", lambda email: True)
    monkeypatch.setattr(routes, "send_promotion_email", lambda email: True)
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    try:
        TEST_DB_PATH.unlink()
    except OSError:
        pass
