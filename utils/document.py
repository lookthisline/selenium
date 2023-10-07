import urllib
import os
import sys
from loguru import logger
import time

__all__ = (
    "download_url_img",
    "save_media"
)


def download_url_img(img_url, img_address):
    response = urllib.request.urlopen(img_url)
    img = response.read()
    with open(img_address, 'wb') as f:
        f.write(img)


def _progress(block_num, block_size, total_size):
    '''回调函数
    @block_num: 已经下载的数据块
    @block_size: 数据块的大小
    @total_size: 远程文件的大小
    '''
    sys.stdout.write('\r>> Downloading %.1f%% ' % (
        float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


def save_media(uri: str, save_path: str):
    """
    http保存媒体文件
    """
    try:
        # 获取save_path的文件夹路径
        dir_path = os.path.dirname(save_path)
        # 如果文件夹不存在则创建
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 判断文件是否存在
        if os.path.exists(save_path):
            print("文件已存在")
            return

        # urllib配置代理
        proxy_handler = urllib.request.ProxyHandler({
            "http": "http://127.0.0.1:7890/",
            "https": "https://127.0.0.1:7890/"
        })
        opener = urllib.request.build_opener(proxy_handler)
        # header配置
        opener.addheaders = [
            ("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
        ]
        urllib.request.install_opener(opener)
        # 下载文件
        print(uri, save_path)
        urllib.request.urlretrieve(uri, save_path, _progress)
        # urllib.request.urlretrieve(uri, save_path)
    except Exception as e:
        logger.exception(e)
        # print(repr(e))
    time.sleep(1)
