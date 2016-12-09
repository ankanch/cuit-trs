import pymysql
import worklib.database as DB

#订阅者的数据库结构为
# email N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 N12 N13 N14 （每一个都代表一种新闻）

def emailCheck(email):
    if email.find('@') <0:
        return False
    if email.find('.',email.find('@')) <0:
        return False
    return True

def reScbscribleCheck(email):
    DBCONN = pymysql.connect(host=DB.DBL_CONNECTION_HOST_CH, port=3306,user=DB.DBL_CONNECTION_USER_CH,passwd=DB.DBL_CONNECTION_PASSWORLD_CH,db=DB.DBL_CONNECTION_DATABASE_NAME_CH,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `news_subscribler` WHERE EMAIL=\""+ email +"\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    emaildata = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(emaildata) > 0:
        return False
    return True

def addToSubscribleList(email,stype):
    if emailCheck(email) == False:
        return "错误！邮件格式不正确。"
    if len(stype) != 14:
        return "非法接口调用！"
    if reScbscribleCheck(email) == False:
        return "你已经订阅了相同内容，请不要重复订阅！"
    tdata = "\""+email+"\","
    #循环获取订阅类别，然后拼接订阅字符串
    for c in stype:
        tdata += "\""+ c +"\","
    tdata = tdata[:len(tdata)-1]
    INS = "INSERT INTO `news_subscribler`(`EMAIL`, `N1`, `N2`, `N3`, `N4`, `N5`, `N6`, `N7`, `N8`, `N9`, `N10`, `N11`, `N12`, `N13`, `N14`) VALUES (" + tdata +")"
    print("Exceute->",INS)
    DBCONN = pymysql.connect(host=DB.DBL_CONNECTION_HOST_CH, port=3306,user=DB.DBL_CONNECTION_USER_CH,passwd=DB.DBL_CONNECTION_PASSWORLD_CH,db=DB.DBL_CONNECTION_DATABASE_NAME_CH,charset='UTF8')
    DBCUR = DBCONN.cursor()
    DBCUR.execute(INS)
    DBCONN.commit()
    emaildata = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return "订阅成功！"

