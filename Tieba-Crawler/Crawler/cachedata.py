import os
#
#该库的作用是缓存数据到到磁盘
#和从磁盘读取数据
#

#下面的路径/命令行在linux环境下需要更改
#下载缓存文件储存文件夹
PATH_DOWNLOADCAHCE = "Cache\\downloads\\" 
CMD_DELFILE = "del Cache\\downloads\\"


#储存文件到磁盘缓存文件夹
def saveToCache(rawdata,filename):
    ff = open(PATH_DOWNLOADCAHCE+filename,"wb")
    ff.write(rawdata)
    ff.close()


#从缓存文件夹读取一个文件,读取成功后函数会删除读取成功的文件
#为了保证replyto字段deep正确性，这个函数还会返回一个值标识当前帖子是否多页（多页的话需要传出帖子ID）
#然后字典存放帖子ID和作者的关系，后面处理根据帖子ID来获取replyto
#如果该函数打开文件失败，说明processWorker处理过快，我们需要sleep5sec等待缓存跟上:第3个为false即可
def readFromCache():
    flist = os.listdir(PATH_DOWNLOADCAHCE)
    if len(flist) == 0:
        return False,False,True
    try:
        ff = open(PATH_DOWNLOADCAHCE+flist[0],"rb")
        htmldata = ff.read()
        ff.close()
    except Exception as e:
        return False,False,False
    delfilecmd = CMD_DELFILE + flist[0]
    os.system(delfilecmd)
    #处理文件名 fxf[帖子ID，当前页数]
    fxf = flist[0].split("-")
    return htmldata,fxf,True


#该函数用来返回缓存数据是否处理完成
def cacheCompleted():
    flist = os.listdir(PATH_DOWNLOADCAHCE)
    if len(flist) == 0:
        return True
    return False