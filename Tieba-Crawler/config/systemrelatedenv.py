# coding=utf-8
#
#
#
#
#运行环境变量，脚本根据不用的运行环境加载不同的配置变量
#默认为windows，可以切换到linux
#
#
#
#
AGV_EXE_ENV_LINUX = False
#
#
#
#
#该脚本定义了在linux以及windows环境下不同命令/变量
#根据config.py中的AGV_EXE_ENV_LINUX来实现切换
#下载缓存文件路径
PATH_DOWNLOADCAHCE = "Cache\\downloads\\"
#任务结果文件夹(每500条进行一次缓存，缓存为一个文件)
PATH_RESULTCACHE = "Cache\\result\\"
#删除文件命令 
CMD_DELFILE = "del Cache\\downloads\\"
#命令行清屏命令
CMD_CLEAR_SCREEN = "cls"
if AGV_EXE_ENV_LINUX == False:
    #下载缓存文件路径
    PATH_DOWNLOADCAHCE = "Cache\\downloads\\"
    #任务结果文件夹(每500条进行一次缓存，缓存为一个文件)
    PATH_RESULTCACHE = "Cache\\result\\"
    #删除文件命令 
    CMD_DELFILE = "del "
    #命令行清屏命令
    CLEAR_SCREEN = "cls"
else:
    #下载缓存文件路径
    PATH_DOWNLOADCAHCE = ".//Cache//downloads//"
    #任务结果文件夹(每500条进行一次缓存，缓存为一个文件)
    PATH_RESULTCACHE = ".//Cache//result//"
    #删除文件命令 
    CMD_DELFILE = "rm "
    #命令行清屏命令
    CMD_CLEAR_SCREEN = "clear"