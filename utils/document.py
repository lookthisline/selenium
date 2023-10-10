import os
import sys
import time
import urllib

import aiohttp
from loguru import logger

__all__ = (
    "download_url_img",
    "save_media",
    "save_media_of_async",
)


def download_url_img(img_url, img_address):
    response = urllib.request.urlopen(img_url)
    img = response.read()
    with open(img_address, 'wb') as f:
        f.write(img)


def _dir_check(dir_path: str):
    """
    检查目录是否存在，不存在则创建
    :param dir_path: 目录路径
    """

    # 获取save_path的文件夹路径
    dir_path = os.path.dirname(dir_path)
    # 如果文件夹不存在则创建
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


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
    http保存媒体文件，异常抛至上层
    :param uri: 网络地址
    :param save_path: 保存路径
    """

    _dir_check(save_path)

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
    time.sleep(1)


async def save_media_of_async(uri: str, save_path: str):
    """
    异步保存媒体文件
    :param uri: 网络地址
    :param save_path: 保存路径
    """

    _dir_check(save_path)

    # 判断文件是否存在
    if os.path.exists(save_path):
        print("文件已存在")
        return

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        headers={
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
    ) as session:
        async with session.get(uri, proxy="http://127.0.0.1:7890/") as response:
            with open(save_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
