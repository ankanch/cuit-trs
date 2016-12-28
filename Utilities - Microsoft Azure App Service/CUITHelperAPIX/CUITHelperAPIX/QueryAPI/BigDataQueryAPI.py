import CUITHelperAPIX.QueryAPI.QueryFunctions as Query
import CUITHelperAPIX.QueryAPI.database as DBS
import pymysql as SQL
import time
import jieba.analyse as ANALYSE
import datetime

#检查hash验证码是否正确
def checkSession(sessiondata):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `bigdata_verify_mail` WHERE SHA1= \"" + sessiondata + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return False  
    timetick = time.time()
    if result[0][5] == True: #判断是否已经验证过
        if result[0][6] == True:
            return False
        return 1
    if result[0][4] + 86400 < timetick:
        UPD = "UPDATE  `bigdata_verify_mail` SET `OUTOFDATE`=True where ID=" + str(result[0][0])
        DBCUR.execute(UPD)
        DBCONN.commit()
        DBCUR.close()
        DBCONN.close()
        return False   #-2为验证过期
    DBCUR.close()
    DBCONN.close()
    return True  #成功返回1

#该函数根据给定id，在bigdata数据库中查找指定用户
def searchForUser(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `tieba_bigdata` WHERE ID= \"" + str(xid) + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return 'NOTFOUND' #未查找到用户
    return result[0][1]


#查询用户的发帖量，给定用户id（已经查询过的ID，然后返回总发帖量和最近30天发帖量）
def getTotalPostsSum(xid):
    count,count30 = Query.countSergent(searchForUser(xid))
    return count ,count30

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

#获取用户活跃时间段
def getActivityTimeZone(xid):
    spostdate = []
    begdate = Query.queryDatasourceEarlyTime()
    spostdate = Query.queryContainListAfterTime(searchForUser(xid),str(begdate))
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

#该函数用来统计满足指定日期的帖子数 *仅用于处理二级数据
#返回值：满足日期的帖子条数
def getCountByDate(date,datalist):
    datedate = date
    ct = 0
    for post in datalist:
        #[[内容,时间],[...],...]
        ddate = post[4]
        if datedate.year == ddate.year and datedate.month == ddate.month and datedate.day == ddate.day:
            ct+=1
    return ct
#获取用户活跃时度
def getActivityTimeLine(xid,days):
    enddate = Query.queryDatasourceLatestTime()
    spostdate = []
    if days > 0:
        begdate = enddate - datetime.timedelta(days=days)
    else:
        begdate = Query.queryDatasourceEarlyTime()
    spostdate = Query.queryContainListAfterTime(searchForUser(xid),str(begdate))
    llen = len(spostdate)
    #开始统计词频
    feqlist = []
    timeline = []
    x = 0
    xdate = begdate
    if days > 30:
        ommit_xlabel_per = days/30  #忽略x label的个数
        ommit_xlabel_per-=1  #同上
        while x<=days:
            feqlist.append(0)
            timeline.append(str(xdate.month)+"-"+str(xdate.day))
            xdate += datetime.timedelta(days=1)
            feqlist[x] = getCountByDate(xdate,spostdate)
            x+=1
            ppp = 0
            while ppp < ommit_xlabel_per and x <= days:
                feqlist.append(0)
                timeline.append("")
                xdate += datetime.timedelta(days=1)
                feqlist[x] = getCountByDate(xdate,spostdate)
                x+=1
                ppp+=1
        xdate -= datetime.timedelta(days=1)
        timeline[len(timeline)-1] == str(xdate.date())
    else:
        while x < days: #初始化频率数组
            feqlist.append(0)
            timeline.append(str(xdate.month)+"-"+str(xdate.day))
            xdate += datetime.timedelta(days=1)
            feqlist[x] = getCountByDate(xdate,spostdate)
            x+=1
    return [timeline,feqlist]

#获取用户关系链
def getReadlationCircle(xid):
    userlist = Query.queryUserListbyReplyto(searchForUser(xid))
    statis = []
    replygotsum = len(userlist)
    for user in userlist:
        exist = False
        i=0
        for pep in statis:
            if pep[0] == user[0]:
                statis[i][1]+=1
                exist = True
                break
            i+=1
        if exist ==False:
            statis.append([user[0],0])
            statis[len(statis)-1][1]+=1
    statis = sorted(statis,key=lambda x:x[1],reverse=True)
    i = 0
    sum = 0
    psum = 0
    label = []
    value = []
    while i<10:
        label.append(statis[i][0])
        value.append(statis[i][1])
        count = statis[i][1]
        per = count/replygotsum*100
        psum += per
        sum += count
        print(statis[i][0],":",count,"\t占",str(int(per))+"%")
        i+=1
    return [label,value]


#获取用户关键字
def getKeymap(xid):
    spostdate = Query.queryWordContainListbyAuthor(searchForUser(xid))
    llen = len(spostdate)
    dp = ""
    #开始统计关键词
    #合并回帖
    for post in spostdate:
        dp += "。" + post[3]
    del spostdate
    kd = ANALYSE.extract_tags(dp, topK=10,allowPOS=( 'n', 'v'))
    feqlist = []
    sumfeq = 0
    for keyword in kd:
        print(keyword,end="\t")
        feqlist.append(0)
    print("\n\n")
    #显示条形图
    #统计词频
    ttt = 0
    for keyword in kd:
        feqlist[ttt] = dp.count(keyword)
        sumfeq+=feqlist[ttt]
        ttt+=1
    return [kd,feqlist]

#获取用户标签
def getTags(xid,seesion):
    pass