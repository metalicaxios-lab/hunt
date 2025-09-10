from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
import threading

class SQLAlchemySingleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = SQLAlchemy()
                    # Configure the MetaData to allow table reloading
                    cls._instance.metadata.clear()
        return cls._instance

db = SQLAlchemySingleton.get_instance()

@contextmanager
def get_db_session():
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
