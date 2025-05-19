# bilibiliDownloader
> 利用bilibili API批量下载
- 视频
- 音频
- 合成音频和视频


## 1. 主要功能

输入视频BV号，批量下载B站视频中的资源，通过在终端中输入不同的参数选择 `仅下载音频 | 仅下载视频 | 下载音频和视频并合成为视频`


https://www.bilibili.com/video/BV1Jg411R7dB/

> bv号（bvid）就是末尾的 BV1Jg411R7dB

```shell
# 下载 BV 号为 BV1Jg411R7dB 视频列表的全部音频，放入 demo 文件夹中
$ python main.py audio --bvid BV1Jg411R7dB --save demo --list
```


```shell
# 下载 BV 号为 BV1eq4y1K7QS 的视频和音频，合成后放入 demo 文件夹中
$ python main.py all --bvid BV1eq4y1K7QS --save demo
```




## 2. Python版本与依赖库

Python 3.8

requests, time, argparse

## 3. 使用方法

1. `clone` 本项目
2. 根据需要选择不同的 `flag ` 运行

```shell
$ python main.py -h                                  
usage: main.py [-h] {audio,video,all} ...

positional arguments:
  {audio,video,all}  commands
    audio            Download only audio file
    video            Download only video file
    all              Download both video and audio file

optional arguments:
  -h, --help         show this help message and exit
  
$ python main.py audio -h
usage: main.py audio [-h] --bvid BVID --save SAVE [--list]

optional arguments:
  -h, --help   show this help message and exit
  --bvid BVID  Enter the 12-bit bvid number
  --save SAVE  Enter the name of your file-dir
  --list       Download a list of videos
```

3. 若使用 `all` flag 运行，则需先下载依赖 [ffmpeg](https://www.ffmpeg.org/download.html) 并将其加入环境变量

