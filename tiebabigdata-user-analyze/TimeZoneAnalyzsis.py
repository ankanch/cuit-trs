import database as DBS
import pymysql as SQL
import time
import QueryFunctions as Query
import datetime
import os
#
#该脚本用于分析每一位用户的活跃时间段
#


#该函数用于按时间排序spostdate
def sortandget(spostdata):
    return sorted(spostdata,key=lambda x:x[4],reverse=True)
#该函数用于将sortandget中的数据按天以每小时分别归类(辅助函数)
def gatherbyDays(sortandgetdata):
    days = [] # [  [date,[ countlist ]    ],    ]
    #建立索引
    for post in sortandgetdata:
        if len(days) != 0:
            NO_FOUND = True
            for ddata in days:
                if ddata[0].year == post[4].year and ddata[0].month == post[4].month and ddata[0].day == post[4].day:
                    NO_FOUND = False
                    break
            if NO_FOUND == True:
                days.append([post[4],[]])
        else:
            days.append([post[4],[]])
    #开始统计
    x = 0
    for ddata in days:
        for post in sortandgetdata:
            if ddata[0].year==post[4].year and ddata[0].month==post[4].month and ddata[0].day == post[4].day:
                timed = post[4].time()
                days[x][1].append(timed)
        x+=1
    return days

#获取用户活跃时间段(需要直接调用这个函数)
def getActivityTimeZone(authorname):
    spostdate = []
    begdate = Query.queryDatasourceEarlyTime()
    spostdate = Query.queryContainListAfterTime(authorname,str(begdate))
    llen = len(spostdate)
    #开始统计词频
    tpostdata = sortandget(spostdate)
    tpostdata = gatherbyDays(tpostdata) # [  [date,[ countlist ]    ],    ]
    FEQLIST = []
    for post in tpostdata:
        feqlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for time in post[1]:
            hour = time.hour
            feqlist[hour]+=1
        FEQLIST.append(feqlist)
    del tpostdata
    #平均下
    avgfeq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    hour = 0
    for x in avgfeq:
        sum = 0
        for hoursum in FEQLIST:
            sum+=hoursum[hour]
        avgfeq[hour] = sum
        hour+=1
    return  avgfeq

#程序主逻辑
DB_NAME = DBS.NAME
DB_HOST = DBS.HOST
DB_USER = DBS.USER
DB_PASSWORD = DBS.PASSWORD

#application start
os.system("cls")
print("cuit tieba user analyzier\nthis script is used to analyze the activity time zone of every user.\napplication start.\nconnecting to the database...")
#==
conn = SQL.connect(host=DB_HOST, port=3306,user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME,charset='UTF8')
conn.set_charset('utf8mb4')
cur = conn.cursor()
print("database connected successfully.\ngenerating diff-user list...")
#==firstly,we have to statistics how many users are in our database
CUS = "SELECT `AUTHOR` FROM `postdata` WHERE 1"
cur.execute(CUS)
authorlist = cur.fetchall()
diffauthor = []
i=0
lenl  = "/" + str(len(authorlist))
print("\n")
for author in authorlist:
    i+=1
    xbuf = " pocessing...  " + str(i) + lenl
    print(xbuf,end="\r")
    if author[0] not in diffauthor:
        diffauthor.append(author[0])
print("diff-user list generated successfully! there are",str(len(diffauthor)),"in total.\nstart retrive keyword for each user...")
#now we have a diff-author list
#let's apply keyword retrive to each user ,then
#==strt poscess
#逐个分析存入数据库
count = 0   # for linux
for author in diffauthor:
    SELPOST = "SELECT `CONTENT` FROM `postdata` WHERE `AUTHOR`=\"" + author +"\""
    #print("querying <",author,"> 's post list...")  #linux下需要注释，否则中文会有问题
    count+=1   #for linux
    print("querying #",count," 's post list...")   #for linux
    cur.execute(SELPOST)
    conn.commit()
    postlist = cur.fetchall()
    print("retrived successfully. <",str(len(postlist)),"> pieces in total")
    print("analyzing...")
    TLM = getActivityTimeZone(author)
    print(TLM)
    INS = "UPDATE `useranalyze` SET `TIMEZONE` =\"" + str(TLM) + "\" WHERE USER=\"" + author + "\""
    cur.execute(INS)
#==pocess finished
print("application completed pocessing.\nclosing session...")
cur.close()
conn.close()
print("application exit.")

