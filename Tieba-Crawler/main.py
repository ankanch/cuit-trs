# coding=utf-8
import Parser.kparser as Parser
import Crawler.cachedata as Cache
import Crawler.kcrawler as Crawler
import Worker.databaseWorker as DBWorker
import Worker.postworker as PostWorker
import Worker.downloadWorker as DownloadWorker
import Config.urls as URL
import threading as Thread
import Config.config as CFG
import time
import os
#调试模块
#from pympler import tracker
import pdb

#贴吧第一页
BEGIN_PAGE =  URL.POST_LIST_SUFFIX
#帖子的地址前缀
POST_SUFFIX = URL.POST_SUFFIX
#并行处理帖子数量
PROCESS_POST_COUNT = CFG.THREAD_PROCESS_POST_COUNT

#tr = tracker.SummaryTracker()
#
#下载模型：一个线程下载帖子列表，另外4个线程分别用来处理每一个帖子
#
os.system(CFG.CMD_CLEAR_SCREEN)
print("CUIT Tieba Crawler\nv1.1 20170205\nkanchisme@gmail.com\n\n")
print("--This crawler will start working now.\n--It will scraping the whole tieba.\n>>>initializing...")
#首先抓取第一页，用来获取贴吧总页数
url = Crawler.urlEncode(BEGIN_PAGE,{'kw':CFG.TIEBA_NAME}) + URL.POST_LIST_PARAMS 
pdata = Crawler.getHtml(url+ "0")
#获取贴吧总页数
postsum = Crawler.getTiebaPageSum(pdata)
#得到第一页的帖子列表
CFG.DATA_POSTLIST = Parser.getPostsList(pdata)
#数据初始化在CFG模块中完成
#输出一次初始化信息
pagesum = int(postsum/50)
print("\tTotal Page:",pagesum,"\tPost Amount in Fitst Page:",len(CFG.DATA_POSTLIST))
###################################################################################################
#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓开始处理：循环下载帖子列表，循环下载帖子，循环匹配数据 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓#
###################################################################################################
#首先开启多个线程处理数据
#创建线程
td = [] #储存帖子下载线程
tp = [] #数据匹配线程
x = 0
print(">>>",CFG.THREAD_DOWNLOAD_POST_LIST_COUNT,"threads allocated for downloading posts.")
while x < CFG.THREAD_DOWNLOAD_POST_LIST_COUNT:
    tn = Thread.Thread(target=DownloadWorker.downloadWorker)
    td.append(tn)
    x+=1
x = 0
print(">>>",CFG.THREAD_PROCESS_POST_COUNT,"threads allocated for processing posts.")
while x < CFG.THREAD_PROCESS_POST_COUNT:
    tn = Thread.Thread(target=PostWorker.processWorker)
    td.append(tn)
    x+=1
#启动线程
print(">>>start threads...")
xxx=1
for item in td:
    item.setDaemon(True)
    item.start()
    if xxx == CFG.THREAD_DOWNLOAD_POST_LIST_COUNT:
        print("\r>>>download threads started. sleep 10 secs for buffer.")
        time.sleep(10)
    xxx+=1
#数据库事务线程，结束条件满足所有退出条件的时候
tn = Thread.Thread(target=DBWorker.databaseWorker)
tn.setDaemon(True)
tn.start()
print("\r>>>database thread started.application will do database job every",CFG.UPDATE_TIMEHOLD,"seconds.")
print("\r>>>threads started")
#接下来开始循环下载帖子列表
print(">>>downloading...\n\n")
curpn = 0
while len(CFG.DATA_POSTLIST) > 0 or Cache.cacheCompleted() == False:
    #将新数据添加到当前的帖子列表尾部
    status = "kanch's high-tech crawler for Tieba is running\nkanchisme@gmail.com\n\n\n"
    status += "\tPostSum:"+str(curpn)+ "/" + str(postsum) + "\n\tPagesDownload:"+ str(CFG.STATUS_PAGES_DOWNLOAD)  \
                + "\n\tPagesProcessed:"+str(CFG.STATUS_PAGES_PROCESS) + "\n\tDataRetrived:"+str(CFG.STATUS_DATA_RETRIVED) +\
                "\n\tDataCached:" + str(CFG.STATUS_DATA_CACHED)
    
    os.system(CFG.CMD_CLEAR_SCREEN)
    print(status + "\n\tDatabaseSubmitted:"+ str(CFG.STATUS_DATA_SUBMITED),end="\n-----\n")
    #这里的结束条件是当pn参数满了的时候就不执行下载了，只更新状态数据
    if curpn <= postsum:
        CFG.DATA_POSTLIST.extend(Parser.getPostsList(Crawler.getHtml(url+ str(curpn))))
        curpn+=50   #百度贴吧URL每一页是按照50递增换页
    else:
        #下载完毕后就2秒刷新一次状态
        time.sleep(2)
    #os.system(CFG.CLEAR_SCREEN)
CFG.STATUS_POSTLIST_DOWNLOAD_COMPLETED = True
#进行最后一次数据更新
while CFG.STATUS_POSTWORKER_FINISHED == False:
    status = "kanch's high-tech crawler for Tieba is running\nkanchisme@gmail.com\n\n\n"
    status += "\tPostSum:"+str(curpn)+ "/" + str(postsum) + "\n\tPagesDownload:"+ str(CFG.STATUS_PAGES_DOWNLOAD)  \
                + "\n\tPagesProcessed:"+str(CFG.STATUS_PAGES_PROCESS) + "\n\tDataRetrived:"+str(CFG.STATUS_DATA_RETRIVED) +\
                "\n\tDataCached:" + str(CFG.STATUS_DATA_CACHED)
    print(status + "\n\tDatabaseSubmitted:"+ str(CFG.STATUS_DATA_SUBMITED),end="\n-----\n")

#进行最后一次提交，将剩余的全部提交
Cache.cacheResultForOnce()
print("\n\twating for database job finished...")
while CFG.STATUS_DATABASE_FINISHED_SUBMIT == False:
    pass
#显示统计信息
status += "\n============\n\n\tPostSum:"+str(curpn)+ "/" + str(postsum) + "\n\tPagesDownload:"+ str(CFG.STATUS_PAGES_DOWNLOAD)  \
         + "\n\tPagesProcessed:"+str(CFG.STATUS_PAGES_PROCESS) + "\n\tDataRetrived:"+str(CFG.STATUS_DATA_RETRIVED)
print(status + "\n\tDatabaseSubmitted:"+ str(CFG.STATUS_DATA_SUBMITED),end="\n-----\n")
print(">>>application finished.")
#tr.print_diff()


