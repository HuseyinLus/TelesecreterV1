import logging
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

# Resolves to TelesecreterV1/data/telesecreter.db
DB_PATH = Path(__file__).parents[3] / "data" / "telesecreter.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_db():
    """
    Context manager that yields a SQLAlchemy Session and handles
    commit/rollback/close automatically.

    Usage:
        with get_db() as session:
            session.add(model)
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error("Database error, rolling back: %s", e)
        raise
    finally:
        session.close()


def check_connection() -> bool:
    """Quick health-check — returns True if the DB is reachable."""
    try:
        with get_db() as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("Database health-check failed: %s", e)
        return False
