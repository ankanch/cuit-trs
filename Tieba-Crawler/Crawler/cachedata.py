# coding=utf-8
import os
import time
import ast
import Config.config as CFG
#
#该库的作用是缓存数据到到磁盘
#和从磁盘读取数据
#

#下面的路径/命令行在linux环境下需要更改
#下载缓存文件储存文件夹
PATH_DOWNLOADCAHCE = CFG.PATH_DOWNLOADCAHCE
CMD_DELFILE = CFG.CMD_DELFILE


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
    i = 0
    while i < len(flist):
        #处理文件名 fxf[帖子ID，当前页数]
        fxf = flist[i].split("-")
        #循环查找文件，需要满足以下条件才会返回：
        #CFG.DATA_PID_PAUTHOR存在key fxf[0]，或fxf[1]为1，即第一页
        if fxf[0] in CFG.DATA_PID_PAUTHOR.keys() or int(fxf[1]) == 1:
            try:
                ff = open(PATH_DOWNLOADCAHCE+flist[i],"rb")
                htmldata = ff.read()
                ff.close()
            except Exception as e:
                print("Cached html File in use.")
                return False,False,False
            delfilecmd = CMD_DELFILE + CFG.PATH_DOWNLOADCAHCE + flist[i]
            os.system(delfilecmd)
            return htmldata,fxf,True
        i+=1
    #上面那个循环理论上是不会跑完的

#该函数用来返回缓存数据是否处理完成
def cacheCompleted():
    flist = os.listdir(PATH_DOWNLOADCAHCE)
    if len(flist) == 0:
        return True
    return False

#该函数用来返回数据缓存数据是否处理完成
def cacheCompleted_Resutl():
    flist = os.listdir(CFG.PATH_RESULTCACHE)
    if len(flist) == 0:
        return True
    return False


#该函数用来储存CFG.DATA_RESULT中的数据到 CFG.PATH_RESULTCACHE目录
#每当CFG.DATA_RESULT的长度满足CFG_UPDATE_CACHE_THROUSHOLD的时候
#就会调用该函数保存数据
def cacheResultForOnce():
    pf = open(CFG.PATH_RESULTCACHE+str(CFG.STATUS_DATA_RETRIVED),"wb")
    pf.write(str(CFG.DATA_RESULT[:CFG.UPDATE_CACHE_THROUSHOLD]).encode("utf-8","ignore"))
    pf.close()
    del CFG.DATA_RESULT[:CFG.UPDATE_CACHE_THROUSHOLD]


#该函数用来从CFG.PATH_RESULTCACHE目录读取缓存的CFG.DATA_RESULT数据
#方便进行数据库事务提交
def readResultFromCache():
    flist = os.listdir(CFG.PATH_RESULTCACHE)
    if len(flist) == 0:
        return False,False
    i = 0
    rd = []
    while i < len(flist):
        try:
            pf = open(CFG.PATH_RESULTCACHE+flist[i],"rb")
            rd = ast.literal_eval(pf.read().decode("utf-8","ignore"))
            pf.close()
        except Exception as e:
            print("Cached result File in use.")
            print(e)
            return False,False
        delfilecmd = CMD_DELFILE + CFG.PATH_RESULTCACHE + flist[i]
        os.system(delfilecmd)
        return rd,True
    i+=1
    #上面那个循环理论上是不会跑完的

