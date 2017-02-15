# coding=utf-8
import Config.systemrelatedenv as STE
import targetTieba 
#该模块定义了在各个模块之间共享的变量
####################################【不可更改变量】################################
#这里的变量为配置项，程序运行时，不应该被更改
#处理每一篇帖子的线程数量(不可更改，只能为1，多线程会导致文件冲突，当前情况下单线程足以)
THREAD_PROCESS_POST_COUNT = 1
#下载帖子列表的线程数量
THREAD_DOWNLOAD_POST_LIST_COUNT = 4
#要抓取的贴吧
TIEBA_NAME = targetTieba.TIEBA_NAME
#TIEBA_NAME = "成都信息工程大学" #长风送远#冰茧的春天#成都信息工程大学
#每当结果集合有指定条数据的时候进行一次数据数据缓存，减少内存占用缓存到文件。
UPDATE_CACHE_THROUSHOLD = 500     
#每当多少秒进行一次数据库提交
UPDATE_TIMEHOLD = 8   
#下面这个用来标识当处理速度快于下载速度的时候等待缓存文件的秒数
PROCESS_WAIT_FOR_CACHE = 8
#下载缓存文件储存文件夹
PATH_DOWNLOADCAHCE = STE.PATH_DOWNLOADCAHCE
#任务结果文件夹(每500条进行一次缓存，缓存为一个文件)
PATH_RESULTCACHE = STE.PATH_RESULTCACHE
#删除文件命令 
CMD_DELFILE = STE.CMD_DELFILE
#命令行清屏命令
CMD_CLEAR_SCREEN = STE.CMD_CLEAR_SCREEN
######################################【状态变量】##################################
#这里的变量是为了能够判断某些条件成立而设立的，在程序运时，可能被更改

#★★★★★储存帖子列表★★★★★
DATA_POSTLIST = []
#★★★★★储存匹配结果（数据库提交事务完成后会删除已经提交的）★★★★★
#结构： [ [帖子ID,当前页码,[replydata]],[帖子ID,当前页码,[replydata]],..... ]
# replydata = [发帖用户,回帖信息,发帖时间,REPLY_TO]
DATA_RESULT = []
#储存帖子ID和楼主的关系，这是个字典 { "帖子ID":楼主,"帖子ID":楼主,... }
#该字典的目的意在处理当一个帖子多于1页的时候，导致后面的页码无法识别楼主
DATA_PID_PAUTHOR = {}
#标记帖子列表是否下载完毕
STATUS_POSTLIST_DOWNLOAD_COMPLETED = False
#标记数据库是否提交完毕
STATUS_DATABASE_FINISHED_SUBMIT = False
#标记postWorker是否处理完毕
STATUS_POSTWORKER_FINISHED = False
#标记当前下载页面数量
STATUS_PAGES_DOWNLOAD = 0
#标记当前处理页面数量
STATUS_PAGES_PROCESS = 0
#标记当前获获取的回帖数量
STATUS_DATA_RETRIVED = 0
#标记已经缓存的结果数量
STATUS_DATA_CACHED = 0
#标记当前获得的帖子数量（一页有50篇帖子）(未使用)
STATUS_POSTLIST_SUM = 0
#标记提交了多少条数据到数据库
STATUS_DATA_SUBMITED = 0


###################################################################################