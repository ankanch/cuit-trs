import Crawler.kcrawler as Crawler
import Crawler.cachedata as Cache
import Config.config as CFG
import Config.urls as URL

#
#该模块是用来处理下载postlist里面的帖子列表的
#可以通过开启多个线程运行work实现高效并发处理

#下载帖子的worker，完成下载postlist中的整个帖子
#结束条件:当页面全部下载完成
#postlist 直接从 config/config.py中的DATA_POSTLIST获取
def downloadWorker():
    print(">>>>>downloadWorker running...")
    while CFG.STATUS_POSTLIST_DOWNLOAD_COMPLETED == False:
        if len(CFG.DATA_POSTLIST) > 0:
            psc = CFG.DATA_POSTLIST[0][1]
            del CFG.DATA_POSTLIST[0]
            psum = Crawler.downloadPost(URL.POST_SUFFIX + psc)
            CFG.STATUS_PAGES_DOWNLOAD += psum