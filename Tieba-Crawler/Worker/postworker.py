import Parser.kparser as Parser
import Crawler.cachedata as Cache
import Config.config as CFG
import time
#测试模块
#import objgraph
#import os
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
        # fxf[帖子ID，当前页数]
        anydata,fxf,success = Cache.readFromCache()
        if success == False:
            time.sleep(CFG.PROCESS_WAIT_FOR_CACHE)
            continue
        if type(anydata) != bool and type(fxf) != bool:
            #os.system("cls")
            #objgraph.show_growth()
            if int(fxf[1]) > 1:
                #replylist = [  [发帖用户,回帖信息,发帖时间,REPLY_TO], [发帖用户,回帖信息,发帖时间,REPLY_TO],... ]
                replylist,firstfloor= Parser.getReplyList(anydata,firstfloor=CFG.DATA_PID_PAUTHOR[fxf[0]])
            else:
                replylist,firstfloor= Parser.getReplyList(anydata)
                #if int(fxf[1]) == 1:
                CFG.DATA_PID_PAUTHOR[fxf[0]] = firstfloor
            #objgraph.show_growth()
            #将结果插入结果集DATA_RESULT
            for madata in replylist:
                #在这里组合成结构： [ [帖子ID,当前页码,[replydata]],[帖子ID,当前页码,[replydata]],..... ]
                # replydata = [发帖用户,回帖信息,发帖时间,REPLY_TO]
                CFG.DATA_RESULT.append([fxf[0],fxf[1],madata])
            rs = len(replylist)
            CFG.STATUS_PAGES_PROCESS += 1
            CFG.STATUS_DATA_RETRIVED += rs
            if CFG.STATUS_DATA_RETRIVED - CFG.STATUS_DATA_CACHED >= CFG.UPDATE_CACHE_THROUSHOLD:
                Cache.cacheResultForOnce()
                CFG.STATUS_DATA_CACHED+=CFG.UPDATE_CACHE_THROUSHOLD
    CFG.STATUS_POSTWORKER_FINISHED = True

