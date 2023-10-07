from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import contextlib

__all__ = (
    "get_element_by_xpath",
    "next_page",
)

url = ""
pc_page_xpath = "/html/body/div[@id='bodywrap']/div[@class='grid']/div[@class='gallary_wrap']/ul[@class='cc']/li"
phone_page_xpath = "/html/body/div/ul[@class='col_2']/li"
pc_next_page_xpath = "/html/body/div[@id='bodywrap']/div[@class='grid']/div[@class='bot_toolbar cc']/div[@class='f_left paginator']/span[@class='next']/a"
phone_next_page_xpath = "/html/body/div[@class='block-pagination']/div[@class='page']/span[@class='next']/a"
current_page_number_xpath = ""


def get_element_by_xpath(driver: WebDriver):
    """
    匹配单页数据
    """
    current_driver_type = None  # 默认为pc
    res = None  # set default value
    with contextlib.suppress(Exception):
        res = driver.find_elements(By.XPATH, pc_page_xpath)
    if not res:
        with contextlib.suppress(Exception):
            res = driver.find_elements(By.XPATH, phone_page_xpath)
        current_driver_type = "phone"

    if not res:
        return
    if current_driver_type is None:
        for item in res:
            pic = item.find_element(
                By.XPATH, "div[@class='pic_box']/a")
            page_link = pic.get_attribute("href")
            pic_title = pic.get_attribute("title")
            pic_uri = pic.find_element(By.XPATH, "img").get_attribute("src")
            pic_info = item.find_element(
                By.XPATH, "div[@class='info']/div[@class='info_col']").text
            data = {
                "page_link": page_link,
                "pic_uri": pic_uri,
                "pic_title": pic_title,
                "pic_info": pic_info,
            }
            yield data
    elif current_driver_type == "phone":
        for item in res:
            pic = item.find_element(By.XPATH, "a[@class='ImgA autoHeight']")

            page_link = pic.get_attribute("href")

            pic_uri_element = pic.find_element(By.XPATH, "img")
            pic_uri = pic_uri_element.get_attribute("src")

            pic_title = item.find_element(By.XPATH, "a[@class='txtA']").text

            pic_info = item.find_element(By.XPATH, "span[@class='info']").text

            data = {
                "page_link": page_link,
                "pic_uri": pic_uri,
                "pic_title": pic_title,
                "pic_info": pic_info,
            }
            yield data


def next_page(driver: WebDriver):
    next_button = None

    # 忽略此处报错
    with contextlib.suppress(Exception):
        next_button = driver.find_element(By.XPATH, pc_next_page_xpath)

    if not next_button:
        # 忽略此处报错
        with contextlib.suppress(Exception):
            next_button = driver.find_element(By.XPATH, phone_next_page_xpath)

    if not next_button:
        return

    next_button.click()
    return driver
