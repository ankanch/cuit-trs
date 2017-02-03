import os
#
#该库的作用是缓存数据到到磁盘
#和从磁盘读取数据
#

#下面的路径/命令行在linux环境下需要更改
#下载缓存文件储存文件夹
PATH_DOWNLOADCAHCE = "Cache/downloads/" 
CMD_DELFILE = "rm Cache/downloads/"


#储存文件到磁盘缓存文件夹
def saveToCache(rawdata,filename):
    ff = open(PATH_DOWNLOADCAHCE+filename,"wb")
    ff.write(rawdata)
    ff.close()


#从缓存文件夹读取一个文件
def readFromCache():
    flist = os.listdir(PATH_DOWNLOADCAHCE)
    if len(flist) == 0:
        return True
    ff = open(dlcachepath+flist[0],"rb")
    htmldata = ff.read()
    ff.close()
    delfilecmd = CMD_DELFILE + flist[0]
    os.system(delfilecmd)
    return htmldata