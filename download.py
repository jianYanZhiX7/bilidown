import os
import time
import random
import requests
import logging
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)
ua = UserAgent()

# 请求间隔配置
MIN_DELAY = 1.0
MAX_DELAY = 3.0

# 代理配置 (使用时取消注释并填写代理地址)
# PROXIES = {
#     'http': 'http://your_proxy_address:port',
#     'https': 'http://your_proxy_address:port'
# }

# Cookie配置 (使用时取消注释并填写真实Cookie)
COOKIE = None  # 默认None，使用时设置为真实Cookie字符串

def random_delay():
    """生成随机延迟"""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    logger.debug(f'随机延迟: {delay:.2f}秒')
    time.sleep(delay)

def make_request(url: str, headers: dict, max_retries: int = 3) -> requests.Response:
    """带重试机制的请求函数
    Args:
        url: 请求URL
        headers: 请求头
        max_retries: 最大重试次数
        
    Returns:
        requests.Response: 响应对象
        
    Raises:
        Exception: 当所有重试都失败时抛出异常
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            # 可在此处添加代理 PROXIES=PROXIES
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.warning(f'请求失败 (尝试 {attempt+1}/{max_retries}): {str(e)}')
            last_exception = e
            if attempt < max_retries - 1:
                random_delay()
    
    raise last_exception if last_exception else Exception('未知错误')

def getAudio(infoList, dirname):
    """下载B站视频的音频文件
    
    Args:
        infoList: 视频信息列表，每个元素为[bvid, cid, title]
        dirname: 保存音频文件的目录
    """
    baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'
    
    if not os.path.exists(dirname):
        logger.info(f'创建音频保存目录: {dirname}')
        os.makedirs(dirname)

    logger.info(f'开始下载音频，共{len(infoList)}个视频')
    
    for idx, item in enumerate(infoList):
        bvid, cid, title = item[0], item[1], item[2]
        logger.info(f'开始处理第{idx+1}个音频: {title} (bvid={bvid})')
        
        st = time.time()
        url = baseUrl + 'bvid=' + bvid + '&cid=' + cid
        logger.debug(f'构造API请求URL: {url}')

        try:
            # 获取音频URL
            headers = {
                'User-Agent': ua.random,
                'Referer': 'https://www.bilibili.com',
                'Origin': 'https://www.bilibili.com'
            }
            logger.debug('请求音频URL...')
            response = make_request(url, headers)
            audioUrl = response.json()['data']['dash']['audio'][0]['baseUrl']
            logger.debug(f'获取到音频URL: {audioUrl}')

            # 下载音频
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Range': 'bytes=0-',
                'Referer': f'https://www.bilibili.com/video/{bvid}',
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive',
                'Cookie': COOKIE if COOKIE else f'buvid3={random.randint(100000,999999)}; buvid_fp={random.randint(100000,999999)}; CURRENT_FNVAL=4048; sid={random.randint(100000,999999)}; fingerprint={random.randint(100000,999999)}',
                'Sec-Fetch-Dest': 'video',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'X-Requested-With': 'com.bilibili.app',
                'DNT': '1',
                'TE': 'trailers',
                'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            }
            # 增加更严格的请求间隔
            delay = random.uniform(3.0, 8.0)
            logger.debug(f'严格随机延迟: {delay:.2f}秒')
            time.sleep(delay)
            
            save_path = os.path.join(dirname, title+'.mp3')
            logger.info(f'开始下载音频到: {save_path}')
            
            with requests.get(audioUrl, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            ed = time.time()
            duration = round(ed - st, 2)
            logger.info(f'音频下载完成: {title}, 耗时: {duration}秒')
            print(f'{duration} seconds download finish: {title}')
            
            time.sleep(1)
            
        except Exception as e:
            logger.error(f'音频下载失败: {title}, 错误: {str(e)}')
            raise


def getVideo(infoList, dirname):
    """下载B站视频的视频文件
    
    Args:
        infoList: 视频信息列表，每个元素为[bvid, cid, title]
        dirname: 保存视频文件的目录
    """
    baseUrl = 'http://api.bilibili.com/x/player/playurl?fnval=16&'
    
    if not os.path.exists(dirname):
        logger.info(f'创建视频保存目录: {dirname}')
        os.makedirs(dirname)

    logger.info(f'开始下载视频，共{len(infoList)}个视频')
    
    for idx, item in enumerate(infoList):
        bvid, cid, title = item[0], item[1], item[2]
        logger.info(f'开始处理第{idx+1}个视频: {title} (bvid={bvid})')
        
        st = time.time()
        url = baseUrl + 'bvid=' + bvid + '&cid=' + cid
        logger.debug(f'构造API请求URL: {url}')

        try:
            # 获取视频URL
            headers = {
                'User-Agent': ua.random,
                'Referer': 'https://www.bilibili.com',
                'Origin': 'https://www.bilibili.com'
            }
            logger.debug('请求视频URL...')
            response = make_request(url, headers)
            videoUrl = response.json()['data']['dash']['video'][0]['baseUrl']
            logger.debug(f'获取到视频URL: {videoUrl}')

            # 下载视频
            headers = {
                'User-Agent': ua.random,
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Range': 'bytes=0-',
                'Referer': 'https://www.bilibili.com/video/' + bvid,
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive',
                'Cookie': COOKIE if COOKIE else '',
                'Sec-Fetch-Dest': 'video',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
            }
            
            save_path = os.path.join(dirname, title+'.mp4')
            logger.info(f'开始下载视频到: {save_path}')
            
            with requests.get(videoUrl, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            ed = time.time()
            duration = round(ed - st, 2)
            logger.info(f'视频下载完成: {title}, 耗时: {duration}秒')
            print(f'{duration} seconds download finish: {title}')
            
            time.sleep(1)
            
        except Exception as e:
            logger.error(f'视频下载失败: {title}, 错误: {str(e)}')
            raise
