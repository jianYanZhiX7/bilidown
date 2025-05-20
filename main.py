import time
import os
import argparse
import subprocess
import shutil
import logging
from datetime import datetime

from geturl import getInformation, getMutipleInformation
from download import getAudio, getVideo

# 配置日志
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/bilidown_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# 不使用 list flag 时，也可以修改代码传入 BVList 列表来下载相互独立的几个视频
# BVList=[
#     'BV1dA411L7Kj','BV1aK4y1a7sd','BV1wf4y1k7as',
#     'BV1CK4y1W7Cc','BV12X4y1K7Ys','BV1Fz4y167Ru',
#     'BV17y4y167xu','BV1wD4y1X7fP','BV1wV41117GP'
# ]

def handle_audio(args):
    """处理音频下载请求
    
    Args:
        args: 命令行参数对象，包含以下属性:
            bvid: 视频BV号
            save: 保存目录
            list: 是否下载列表标志
    """
    logger.info('开始音频下载任务')
    logger.info(f'参数: bvid={args.bvid}, save={args.save}, list={args.list}')

    st = time.time()

    try:
        if args.list:
            logger.info('正在下载视频列表音频...')
            getAudio(getMutipleInformation(args.bvid), args.save)
        else:
            logger.info('正在下载单个视频音频...')
            getAudio(getInformation([args.bvid]), args.save)
    except Exception as e:
        logger.error(f'音频下载失败: {str(e)}')
        raise

    ed = time.time()
    duration = round(ed - st, 2)
    logger.info(f'音频下载完成! 耗时: {duration}秒')
    print(f'Download Finish All! Time consuming: {duration} seconds')


def handle_video(args):
    """处理视频下载请求
    
    Args:
        args: 命令行参数对象，包含以下属性:
            bvid: 视频BV号
            save: 保存目录
            list: 是否下载列表标志
    """
    logger.info('开始视频下载任务')
    logger.info(f'参数: bvid={args.bvid}, save={args.save}, list={args.list}')

    st = time.time()

    try:
        if args.list:
            logger.info('正在下载视频列表...')
            getVideo(getMutipleInformation(args.bvid), args.save)
        else:
            logger.info('正在下载单个视频...')
            getVideo(getInformation([args.bvid]), args.save)
    except Exception as e:
        logger.error(f'视频下载失败: {str(e)}')
        raise

    ed = time.time()
    duration = round(ed - st, 2)
    logger.info(f'视频下载完成! 耗时: {duration}秒')
    print(f'Download Finish All! Time consuming: {duration} seconds')


def handle_all(args):
    """处理音视频下载及合并请求
    
    Args:
        args: 命令行参数对象，包含以下属性:
            bvid: 视频BV号
            save: 保存目录
            list: 是否下载列表标志
    """
    logger.info('开始音视频下载及合并任务')
    logger.info(f'参数: bvid={args.bvid}, save={args.save}, list={args.list}')

    st = time.time()

    try:
        if not os.path.exists('temp'):
            logger.info('创建临时目录: temp')
            os.makedirs('temp')
        if not os.path.exists(args.save):
            logger.info(f'创建输出目录: {args.save}')
            os.makedirs(args.save)

        # 下载音视频
        if args.list:
            logger.info('开始下载视频列表的音视频...')
            getAudio(getMutipleInformation(args.bvid), 'temp')
            getVideo(getMutipleInformation(args.bvid), 'temp')
        else:
            logger.info('开始下载单个视频的音视频...')
            getAudio(getInformation([args.bvid]), 'temp')
            getVideo(getInformation([args.bvid]), 'temp')

        # 合并音视频
        logger.info('开始合并音视频...')
        names = os.listdir('temp')
        for name in names:
            if name.split('.')[-1] == 'mp4':
                logger.info(f'正在合并文件: {name}')
                subprocess.call(
                    f'ffmpeg -i temp/{name} -i temp/{name[:-4]}.mp3 -codec copy {os.path.join(args.save, name)}'
                )
        
        # 清理临时目录
        logger.info('清理临时目录...')
        shutil.rmtree('temp')

    except Exception as e:
        logger.error(f'音视频处理失败: {str(e)}')
        raise

    ed = time.time()
    duration = round(ed - st, 2)
    logger.info(f'音视频处理完成! 总耗时: {duration}秒')
    print(f'Download Finish All! Time consuming: {duration} seconds')



def main():
    """主函数，解析命令行参数并执行相应功能"""
    logger.info('B站音视频下载器启动')
    
    try:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='commands')

        # 配置音频下载参数
        audio_parser = subparsers.add_parser(name='audio', help='Download only audio file')
        audio_parser.add_argument('--bvid', required=True, help="Enter the 12-bit bvid number")
        audio_parser.add_argument('--save', required=True, help="Enter the name of your file-dir")
        audio_parser.add_argument('--list', action="store_true", help="Download a list of videos")
        audio_parser.set_defaults(func=handle_audio)

        # 配置视频下载参数
        video_parser = subparsers.add_parser(name='video', help='Download only video file')
        video_parser.add_argument('--bvid', required=True, help="Enter the 12-bit bvid number")
        video_parser.add_argument('--save', required=True, help="Enter the name of your file-dir")
        video_parser.add_argument('--list', action="store_true", help="Download a list of videos")
        video_parser.set_defaults(func=handle_video)

        # 配置音视频合并参数
        all_parser = subparsers.add_parser(name='all', help='Download both video and audio file')
        all_parser.add_argument('--bvid', required=True, help="Enter the 12-bit bvid number")
        all_parser.add_argument('--save', required=True, help="Enter the name of your file-dir")
        all_parser.add_argument('--list', action="store_true", help="Download a list of videos")
        all_parser.set_defaults(func=handle_all)

        args = parser.parse_args()
        logger.info(f'解析命令行参数完成，执行功能: {args.func.__name__}')
        
        # 执行功能函数
        args.func(args)
        
    except Exception as e:
        logger.error(f'程序运行出错: {str(e)}')
        raise


if __name__ == '__main__':
    logger.info('='*50)
    logger.info('程序启动')
    main()
    logger.info('程序正常退出')
