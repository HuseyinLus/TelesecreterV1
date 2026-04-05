import sqlite3
import logging
from pathlib import Path
from contextlib import contextmanager
 
logger = logging.getLogger(__name__)
 
# Resolves to TelesecreterV1/data/telesecreter.db
DB_PATH = Path(__file__).parents[3] / "data" / "telesecreter.db"
 
# Ensure the data directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
 
 
def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite connection.
    - Row factory set so rows behave like dicts (access by column name).
    - Foreign key enforcement enabled per connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
 
@contextmanager
def get_db():
    """
    Context manager that yields a connection and handles
    commit/rollback/close automatically.
 
    Usage:
        with get_db() as conn:
            conn.execute("INSERT INTO ...")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Database error, rolling back: %s", e)
        raise
    finally:
        conn.close()
 
 
def init_db(schema_path: Path | None = None) -> None:
    """
    Initialize the database by running a SQL schema file.
 
    Args:
        schema_path: Path to the .sql schema file.
                     Defaults to schema.sql in the same directory.
    """
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"
 
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
 
    with get_db() as conn:
        sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql)
 
    logger.info("Database initialized from %s", schema_path)
 
 
def check_connection() -> bool:
    """
    Quick health-check — returns True if the DB is reachable.
    """
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error("Database health-check failed: %s", e)
        return False