from ..engine import SQLiteBase

from sqlalchemy import (
    Column,
    Integer,
    Text,
)


class Picture(SQLiteBase):
    __tablename__ = "picture"
    __table_args__ = (
        {"sqlite_autoincrement": True}
    )

    id = Column(Integer, primary_key=True)
    pic_title = Column(Text, nullable=False, unique=True)
    page_link = Column(Text, nullable=False)
    pic_uri = Column(Text, nullable=False)
    pic_info = Column(Text, nullable=False)


SQLiteBase.metadata.create_all()
