import requests
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

def getCidAndTitle(bvid, p=1):
    """获取B站视频的CID和标题
    
    Args:
        bvid: 视频BV号
        p: 分P序号，默认为1
        
    Returns:
        tuple: (cid, title) 视频CID和标题
    """
    logger.info(f'开始获取视频信息: bvid={bvid}, p={p}')
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com'
    }
    
    try:
        logger.debug(f'请求API: {url}')
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['data']
        
        title = data['title']
        cid = data['pages'][p-1]['cid']
        
        logger.info(f'获取成功: title={title}, cid={cid}')
        return str(cid), title
        
    except Exception as e:
        logger.error(f'获取视频信息失败: {str(e)}')
        raise

def getInformation(bvList):
    """获取单个或多个B站视频的信息列表
    
    Args:
        bvList: 视频BV号列表，可以是单个视频或多P视频
        
    Returns:
        list: 包含视频信息的列表，每个元素为[bvid, cid, title]
    """
    logger.info(f'开始处理视频信息列表，共{len(bvList)}个视频')
    infoList = []
    
    try:
        for idx, bvid in enumerate(bvList):
            logger.debug(f'正在处理第{idx+1}个视频: {bvid}')
            item = []
            
            if len(bvid) == 12:
                logger.debug('处理单个视频')
                cid, title = getCidAndTitle(bvid)
                item.append(bvid)
            else:
                logger.debug('处理多P视频')
                cid, title = getCidAndTitle(bvid[:12], int(bvid[13:]))
                item.append(bvid[:12])
                
            item.append(cid)
            item.append(title)
            infoList.append(item)
            
        logger.info(f'成功处理所有视频信息，共获取{len(infoList)}条记录')
        return infoList
        
    except Exception as e:
        logger.error(f'处理视频信息列表失败: {str(e)}')
        raise

def getMutipleInformation(bvid):
    """获取B站多P视频的所有分P信息
    
    Args:
        bvid: 视频BV号
        
    Returns:
        list: 包含所有分P信息的列表，每个元素为[bvid, cid, title]
    """
    logger.info(f'开始获取多P视频信息: bvid={bvid}')
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com'
    }
    
    try:
        logger.debug(f'请求API: {url}')
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['data']
        
        infoList = []
        total_pages = len(data['pages'])
        logger.info(f'共发现{total_pages}个分P视频')
        
        for idx, page in enumerate(data['pages']):
            title = page['part']
            cid = str(page['cid'])
            item = [bvid, cid, title]
            infoList.append(item)
            logger.debug(f'已处理第{idx+1}个分P: {title} (cid={cid})')
            
        logger.info(f'成功获取所有分P信息，共{len(infoList)}条记录')
        return infoList
        
    except Exception as e:
        logger.error(f'获取多P视频信息失败: {str(e)}')
        raise
