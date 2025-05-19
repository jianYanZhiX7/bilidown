import os
import time
import requests
import logging

logger = logging.getLogger(__name__)

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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Referer': 'https://www.bilibili.com',
                'Origin': 'https://www.bilibili.com'
            }
            logger.debug('请求音频URL...')
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            audioUrl = response.json()['data']['dash']['audio'][0]['baseUrl']
            logger.debug(f'获取到音频URL: {audioUrl}')

            # 下载音频
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Range': 'bytes=0-',
                'Referer': 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid,
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive'
            }
            
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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Referer': 'https://www.bilibili.com',
                'Origin': 'https://www.bilibili.com'
            }
            logger.debug('请求视频URL...')
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            videoUrl = response.json()['data']['dash']['video'][0]['baseUrl']
            logger.debug(f'获取到视频URL: {videoUrl}')

            # 下载视频
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Range': 'bytes=0-',
                'Referer': 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid,
                'Origin': 'https://www.bilibili.com',
                'Connection': 'keep-alive'
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
