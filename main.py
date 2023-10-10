import asyncio
import hashlib
import os
import re
import time

from loguru import logger
from sqlalchemy.orm import Session

from db.session import sqlite_session
from db.sqlite.picture import fine_record, save_data
from driver.chrome import chrome_driver
from spider.wn import get_element_by_xpath, next_page, url
from utils.document import save_media, save_media_of_async

# 保存到当前目录的images文件夹下
SAVE_DIR = os.path.join(os.getcwd(), 'images\\')


def save_page_data(session: Session, res: list = []):
    if not res:
        return
    for item in res:
        if fine_record(session, item["pic_title"]) is not None:
            continue
        save_data(session, item)


async def save_pic(res: list = []):
    for item in res:
        # 获取文件后缀
        suffix = item['pic_uri'].split(".")[-1]
        file_name = item['pic_title'][:250] + "." + suffix  # 限制文件名长度，预留5个字符给后缀
        file_name = re.sub(r'[\\/:*?"<>|]', '', file_name)  # 去除非法字符
        # 备选名称
        file_name_2 = re.findall(
            r'\d+', item["page_link"])[0]  # 提取其中的数字部分

        # 提前校验备选名称是否已存在
        if os.path.exists(SAVE_DIR + file_name_2 + "." + suffix):
            print("文件已存在")
            return

        if not file_name_2:
            # 使用hash时间字符串为文件名
            file_name_2 = hashlib.md5(
                str(time.time()).encode('utf-8')).hexdigest()
        try:
            await save_media_of_async(
                item['pic_uri'], SAVE_DIR + file_name)  # 保存到正常名称
        except OSError as e:
            logger.error(e)
            await save_media_of_async(item["pic_uri"], SAVE_DIR +
                                      file_name_2 + "." + suffix)  # 保存到备选名称
        except Exception as e:
            logger.exception(e)


def wn():
    try:
        driver = chrome_driver()
        driver.get(url)  # home page
        # ----------

        # print driver uri
        logger.debug(driver.current_url)

        res = [i for i in get_element_by_xpath(driver) if i]
        session: Session = next(sqlite_session())
        save_page_data(session, res)  # save main page data
        asyncio.run(save_pic(res))  # save pic

        max_read_page = 10
        current_page = 0
        current_driver = driver

        while current_page < max_read_page:
            # next page
            next_driver = next_page(current_driver)
            # print driver uri
            logger.debug(next_driver.current_url)
            res = [i for i in get_element_by_xpath(next_driver) if i]
            save_page_data(session, res)
            asyncio.run(save_pic(res))
            current_driver = next_driver
            current_page += 1

        # ----------
        driver.quit()
    except Exception as e:
        logger.exception(e)


def test():
    pass


if __name__ == '__main__':
    wn()
