import datasourceconfig.database_settings as DBS
import pymysql as SQL
import datetime

#从数据库加载指定条数的曝光数据，按照时间排序
def queryBadposts(qsum):
    pass


#插入新的曝光数据到数据库
def insertBadposts(title,content):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "INSERT INTO `badposts`(`TITLE`, `CONTENT`, `DATE`, `UP`) VALUES (\""
    INS = INS + title +"\",\"" + content + "\",\"" + str(datetime.datetime.now()) + "\",1)"
    DBCUR.execute(INS)
    DBCONN.commit()
    SEL = "SELECT `ID` FROM `badposts` WHERE TITLE=\"" + title +"\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result[0][0]

#获取指定曝光的信息
def getBadposts(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "SELECT * FROM `badposts` WHERE ID=" + str(xid)
    DBCUR.execute(INS)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result[0]


#搜索包含指定关键字的曝光数据
def searchFor(tags):
    pass

#支持了某一篇曝光
def support(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `badposts` WHERE  ID= " + str(xid)
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return False   #false为未查找到指定回帖
    ADD = "UPDATE `badposts` SET `UP`=`UP`+1 WHERE `ID`=" + str(id)
    DBCUR.execute(ADD)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    return True


###########################3
#数据库辅助函数
###########################