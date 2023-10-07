from driver.chrome import chrome_driver
from spider.wn import get_element_by_xpath, url, next_page
from db.session import sqlite_session
from loguru import logger
from sqlalchemy.orm import Session
from utils.document import save_media
from db.sqlite.picture import fine_record, save_data
import os


def save_page_data(session: Session, res: list = []):
    if not res:
        return
    for item in res:
        if fine_record(session, item["pic_title"]) is not None:
            continue
        save_data(session, item)


def save_pic(res: list = []):
    for item in res:
        # 获取文件后缀
        suffix = item['pic_uri'].split(".")[-1]
        file_name = item['pic_title'][:250] + "." + suffix  # 限制文件名长度，预留5个字符给后缀
        save_media(item['pic_uri'], SAVE_DIR + file_name)


# 保存到当前目录的images文件夹下
SAVE_DIR = os.path.join(os.getcwd(), 'images\\')

if __name__ == '__main__':
    try:
        driver = chrome_driver()
        driver.get(url)  # home page
        # ----------

        res = [i for i in get_element_by_xpath(driver) if i]
        session: Session = next(sqlite_session())
        save_page_data(session, res)  # save main page data
        save_pic(res)  # save pic

        max_read_page = 10
        current_page = 0
        current_driver = driver

        while current_page < max_read_page:
            # next page
            d = next_page(current_driver)
            res = [i for i in get_element_by_xpath(d) if i]
            save_page_data(session, res)
            save_pic(res)
            current_driver = d
            current_page += 1

        # ----------
        driver.quit()
    except Exception as e:
        logger.exception(e)