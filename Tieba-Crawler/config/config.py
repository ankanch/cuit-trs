#该模块定义了在各个模块之间共享的变量
####################################【不可更改变量】################################
#这里的变量为配置项，程序运行时，不应该被更改
#处理每一篇帖子的线程数量(建议为1，多线程会导致缓冲不足，出错)
THREAD_PROCESS_POST_COUNT = 1
#下载帖子列表的线程数量
THREAD_DOWNLOAD_POST_LIST_COUNT = 4
#要抓取的贴吧
TIEBA_NAME = "成都信息工程大学"
#每当结果集合有指定条数据的时候进行一次数据库提交事务
UPDATE_THROUSHOLD = 200        
#下面这个用来标识当处理速度快于下载速度的时候等待缓存文件的秒数
PROCESS_WAIT_FOR_CACHE = 5

CLEAR_SCREEN = "cls"
CLEAR_SCREEN_LINUX = "clear"
######################################【状态变量】##################################
#这里的变量是为了能够判断某些条件成立而设立的，在程序运时，可能被更改

#★★★★★储存帖子列表★★★★★
DATA_POSTLIST = []
#★★★★★储存匹配结果（数据库提交事务完成后会删除已经提交的）★★★★★
#结构： [ [帖子ID,当前页码,[replydata]],[帖子ID,当前页码,[replydata]],..... ]
# replydata = [发帖用户,回帖信息,发帖时间,REPLY_TO]
DATA_RESULT = []
#标记帖子列表是否下载完毕
STATUS_POSTLIST_DOWNLOAD_COMPLETED = False
#标记当前下载页面数量
STATUS_PAGES_DOWNLOAD = 0
#标记当前处理页面数量
STATUS_PAGES_PROCESS = 0
#标记当前获获取的回帖数量
STATUS_DATA_RETRIVED = 0
#标记当前获得的帖子数量（一页有50篇帖子）(未使用)
STATUS_POSTLIST_SUM = 0


###################################################################################