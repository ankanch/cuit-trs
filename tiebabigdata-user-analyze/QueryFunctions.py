import pymysql
import datetime
import database as DBS


#该函数用来查询指定字段在数据库中的出现次数
def countSergent(value):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    latestdate = queryDatasourceLatestTime()
    begdate = latestdate - datetime.timedelta(days=30)
    SEL = "SELECT COUNT(AUTHOR) FROM `postdata`  WHERE AUTHOR=\"" + value + "\" and DATE>'" + str(begdate) + "'"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    count30 = DBCUR.fetchall()
    SEL = "SELECT COUNT(AUTHOR) FROM `postdata`  WHERE AUTHOR=\"" + value + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    count = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return count[0][0],count30[0][0]

#从数据库查询包含指定字词的所有数据集
#返回值：包含指定字词的数据集列表
def queryWordContainListbyKeyword(word):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select  CONTENT from `postdata`    where CONTENT like('%" + word +"%')"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist

#从数据库查询指定作者的所有帖子信息
#返回值：指定作者的所有回帖信息
# [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
def queryWordContainListbyAuthor(author):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select  * from `postdata`    where AUTHOR=\"" + author +"\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist

#从数据库查询回复给指定用户的所有其它用户列表
#返回值：用户列表 
# [ "1","2",....]
def queryUserListbyReplyto(author):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select  AUTHOR from `postdata`    where REPLYTO=\"" + author +"\" and AUTHOR!=\"" + author + "\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist

#从数据库查询指定用户回复给指定用户的帖子列表
#返回值：贴子列表
# [ "1","2",....]
def queryContentListbyAuthorToReplyto(fromauthor,toauthor):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select  CONTENT from `postdata`    where REPLYTO=\"" + toauthor +"\" and AUTHOR!=\"" + fromauthor + "\""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist

#从数据库查询最大日期
#返回值：一个最大日期
def queryDatasourceLatestTime():
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select MAX(DATE) from `postdata`"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist[0][0]

#从数据库查询小日期
#返回值：一个最小日期
def queryDatasourceEarlyTime():
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select MIN(DATE) from `postdata`"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return datalist[0][0]

#从数据库查询指定作者的指定日期之间的数据集
#返回值：指定日期之间的数据集列表
# [ [主题帖链接,贴吧名,作者,帖子内容,发帖时间,回复给sb,所在页面],[......],..... ]
def queryContainListAfterTime(author,earlydatestr):
    DBCONN = pymysql.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "select *   from `postdata`   where AUTHOR=\"" + author + "\" and DATE>'" + earlydatestr + "'"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(SEL)
    DBCONN.commit()
    datalist = DBCUR.fetchall()
    #print(len(datalist))
    DBCUR.close()
    DBCONN.close()
    return datalist

