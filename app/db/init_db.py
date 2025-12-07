"""Initialize database."""

from sqlmodel import SQLModel

from app.db.session import engine
from app.modules.machine.model.machine_model import Machine  # noqa: F401


def init_db():
    """Initialize database."""
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
