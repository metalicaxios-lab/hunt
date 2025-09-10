from functools import wraps
from flask import g
from api.models import db

def with_db_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get the scoped session
            session = getattr(g, 'db_session', db.session)
            # Add session to kwargs
            kwargs['session'] = session
            return f(*args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
    return decorated_function
