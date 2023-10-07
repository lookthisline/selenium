from sqlalchemy.orm import sessionmaker
from db.engine import define_session_sqlite
from loguru import logger

__all__ = (
    'sqlite_session',
)


class get_session:
    def __init__(self, eng: sessionmaker, autocommit: bool = False):
        self.autocommit = autocommit
        self.eng = eng

    def __call__(self):
        self.eng.configure(autocommit=False, autoflush=False)
        session = self.eng()
        try:
            yield session
            if self.autocommit:
                session.commit()
        except Exception as e:
            logger.error(e)
            if self.autocommit:
                session.rollback()
        finally:
            session.close()


sqlite_session = get_session(define_session_sqlite)
