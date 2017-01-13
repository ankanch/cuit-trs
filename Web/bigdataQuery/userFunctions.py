import datasourceconfig.database_settings as DBS
import pymysql as SQL
import random

#这个文件是一些用来查找用户，向bigdata插入用户的函数
def checkUser(username):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `tieba_bigdata` WHERE TIEBAID= \"" + username + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return -1 #未查找到用户
    return result[0][0]

#
def insertIntoBigData(username):
    DBCONN = SQL.connect(host=DBS.HOST_TB, port=3306,user=DBS.USER_TB,passwd=DBS.PASSWORD_TB,db=DBS.NAME_TB,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `postdata` WHERE AUTHOR= \"" + username + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return -1 #未查找到用户
    NAME = result[0][2]
    DBCUR.close()
    DBCONN.close()
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "INSERT INTO `tieba_bigdata`(`TIEBAID`, `REALNAME`, `XUEHAO`, `CONTACT_QQ`, `CONTACT_PHONE`, `CONTACT_EMAIL`, `COLLEGE`, `GRADECLASS`, `TAGS`, `KEYWORD`) VALUES ("
    INS = INS + "\"" + username +"\",\"未知\",0,0,\"未知\",\"未知\",\"未知\",\"未知\",\"无数据\",\"无数据\")" 
    DBCUR.execute(INS)
    DBCONN.commit()
    SEL = "SELECT `ID` FROM `tieba_bigdata` WHERE TIEBAID= \"" + username + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    uid = result[0][0]
    DBCUR.close()
    DBCONN.close()
    return uid

#该函数用来获取用户的一些基本信息
def getBasicInfo(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `tieba_bigdata` WHERE ID= \"" + xid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return [False]
    return result[0]


#该函数用于随机抽取10条用户发帖记录
def getRandom10Post(xid):
    #获取用户名
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT `TIEBAID` FROM `tieba_bigdata` WHERE ID= \"" + xid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return "无发帖信息"
    DBCONN = SQL.connect(host=DBS.HOST_TB, port=3306,user=DBS.USER_TB,passwd=DBS.PASSWORD_TB,db=DBS.NAME_TB,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT `CONTENT`,`DATE` FROM `postdata` WHERE AUTHOR= \"" + result[0][0] + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    i=0
    rstr = ""
    HEAD = """ <div class="alert alert-dismissible alert-info">"""
    TAIL = """</div>"""
    print(len(result))
    while i< 10 and i<len(result):
        rs = str(result[random.randint(0, len(result)-1)][1])  + ": " + str(result[random.randint(0, len(result)-1)][0])
        i+=1
        rstr += ( HEAD + rs + TAIL)
    return rstr