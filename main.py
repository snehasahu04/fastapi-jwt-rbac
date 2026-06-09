from fastapi import FastAPI
from sqlalchemy import inspect
import models
from database import engine
from routes import router


def ensure_db_schema():
    inspector = inspect(engine)
    if "users" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("users")]
        if "hashed_password" not in columns:
            models.Base.metadata.drop_all(bind=engine)
            models.Base.metadata.create_all(bind=engine)
    else:
        models.Base.metadata.create_all(bind=engine)


ensure_db_schema()

app = FastAPI()

app.include_router(router)