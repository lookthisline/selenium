from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

__all__ = (
    "set_chrome_options",
    "chrome_driver",
)


def set_chrome_options() -> Options:
    """
    设置浏览器参数
    """
    options = Options()
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # options.add_argument('--headless') # 无头参数
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument(
        "--proxy-server=http://127.0.0.1:7890;https://127.0.0.1:7890")  # 设置代理
    # options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    options.add_argument('--start-maximized')  # 全屏显示
    options.add_argument('lang=zh_CN.UTF-8')  # 设置编码
    options.add_argument('incognito')  # 隐身模式（无痕模式）
    options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    # options.add_experimental_option('detach', True)  # 保持浏览器不退出
    return options


def chrome_driver(implicitly_wait_second: int = 10) -> WebDriver:
    """
    设置浏览器驱动
    :param implicitly_wait_second: 隐式等待时间
    """
    # driver = WebDriver(options=set_chrome_options())
    # driver.implicitly_wait(implicitly_wait_second)
    # return driver

    return WebDriver(options=set_chrome_options())
