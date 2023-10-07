from typing import List
from sqlalchemy.orm import Session
from ..define.sqlite import Picture

__all__ = (
    "fine_record",
    "save_data",
    "save_all_data",
    "get_all_data",
)


def fine_record(session: Session, title: str = ""):
    if not title:
        return None
    return session.query(Picture).filter(Picture.pic_title == title).first()


def save_data(session: Session, data: dict = {}):
    if not data:
        return
    row = Picture(
        page_link=data["page_link"],
        pic_uri=data["pic_uri"],
        pic_title=data["pic_title"],
        pic_info=data["pic_info"],
    )
    session.add(row)
    session.commit()


def save_all_data(session: Session, data: List[dict] = []):
    row_list = [
        Picture(
            page_link=item["page_link"],
            pic_uri=item["pic_uri"],
            pic_title=item["pic_title"],
            pic_info=item["pic_info"],
        ) for item in data if item
    ]
    if not row_list:
        return
    session.add_all(row_list)
    session.commit()


def get_all_data(session: Session):
    return session.query(Picture).all()
