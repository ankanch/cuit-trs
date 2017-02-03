import Parser.kparser as Parser
import Crawler.cachedata as Cache
import Config.config as CFG

#
#该脚本是用来处理帖子数据的
#可以通过开启多个线程运行work实现高效并发处理

#处理的worker，完成匹配出所有数据的任务
#结束条件:当页面全部下载完成且Cache/downloads/文件夹没有文件
#数据源：Cache/downloads/文件夹下的文件
def processWorker():
    print(">>>>>processWorker running...")
    #退出该函数既要保证全部下载完毕，又要保证缓存文件全部处理完毕
    while CFG.STATUS_POSTLIST_DOWNLOAD_COMPLETED == False or Cache.cacheCompleted() == False:
        anydata = Cache.readFromCache()
        if type(anydata) != bool:
            replylist,firstfloor= Parser.getReplyList(anydata)
            rs = len(replylist)
            CFG.STATUS_PAGES_PROCESS += 1
            CFG.STATUS_DATA_RETRIVED += rs