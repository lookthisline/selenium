from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = (
    "define_session_sqlite",
)

sqlite_engine = create_engine(
    'sqlite:///db/data/wn.db', connect_args={"check_same_thread": False}, echo=False)
define_session_sqlite = sessionmaker(bind=sqlite_engine)
SQLiteBase = declarative_base(bind=sqlite_engine)
