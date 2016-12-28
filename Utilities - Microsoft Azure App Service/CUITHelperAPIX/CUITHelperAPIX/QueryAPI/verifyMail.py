from CUITHelperAPIX.QueryAPI import database as DBS
import pymysql as SQL
import time

#该库用来生成和验证hash
#每个hash由 时间戳（秒），邮箱地址，查找目标，组成
#过期时间，每个hash有效时间为24小时（86400秒）
def checkHash(hashdata):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORLD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    DBCUR.execute("SET names 'utf8mb4'")
    SEL = "SELECT * FROM `bigdata_verify_mail` WHERE SHA1= \"" + hashdata + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return -1   #-1为为查找到指定hash
    timetick = time.time()
    if result[0][5] == True: #判断是否已经验证过
        if result[0][6] == True:
            return -2
        return 1
    if result[0][4] + 86400 < timetick:
        UPD = "UPDATE  `bigdata_verify_mail` SET `OUTOFDATE`=True where ID=" + str(result[0][0])
        DBCUR.execute(UPD)
        DBCONN.commit()
        DBCUR.close()
        DBCONN.close()
        return -2   #-2为验证过期
    UPD = "UPDATE  `bigdata_verify_mail` SET `VERIFIED`=True where ID=" + str(result[0][0])
    DBCUR.execute(UPD)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    return 1  #成功返回1

#该函数用来检测session是否正确
#超过24小时，就返回错误
#session未验证返回错误
def checkSession(sessiondata):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    SEL = "SELECT * FROM `bigdata_verify_mail` WHERE SHA1= \"" + sessiondata + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return -1   #-1为为查找到指定hash
    timetick = time.time()
    if result[0][5] == True: #判断是否已经验证过
        if result[0][6] == True:
            return -2
        return 1
    if result[0][4] + 86400 < timetick:
        UPD = "UPDATE  `bigdata_verify_mail` SET `OUTOFDATE`=True where ID=" + str(result[0][0])
        DBCUR.execute(UPD)
        DBCONN.commit()
        DBCUR.close()
        DBCONN.close()
        return -2   #-2为验证过期
    DBCUR.close()
    DBCONN.close()
    return 1  #成功返回1
