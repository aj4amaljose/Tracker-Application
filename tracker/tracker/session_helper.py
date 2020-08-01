"""
Helps to create maintain session
"""
import functools
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


@contextmanager
def session_scope(session):
    """
    Manages session during function execution
    """
    try:
        yield
    except:
        session.rollback()
    finally:
        session.commit()
        session.close()


def create_session(engine):
    """

    """
    session_ = sessionmaker(bind=engine)
    session = session_()

    def with_session_scope(func):
        @functools.wraps(func)
        def process(*args, **kwargs):
            with session_scope(session):
                return func(session, *args, **kwargs)

        return process

    return with_session_scope

