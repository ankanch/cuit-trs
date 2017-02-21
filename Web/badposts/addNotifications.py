import pymysql as SQL
import datasourceconfig.database_settings as DBS

#该脚本的目的只有一个，那就是将一条新的回复ID插入一个用户的MessageBox里面
#传入目标回复id以及新回复ID
def NotifyUser(rid,msgid,rof):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    result = []
    if int(rid) == 0:
        #如果回复的是主题帖，那么
        #首先获取发帖人的UID
        SEL = "SELECT `UID` FROM `badposts` WHERE ID=" + str(rof)
        print(SEL)
        DBCUR.execute(SEL)
        DBCONN.commit()
        result = DBCUR.fetchall()
    else:
        #获取rid帖子（回复目标）的发帖用户ID
        SEL = "SELECT `UID` FROM `badposts_reply` WHERE `ID`=" + str(rid)
        print(SEL)
        DBCUR.execute(SEL)
        DBCONN.commit()
        result = DBCUR.fetchall()
    print(result)
    uid = result[0][0]
    #回复的回复
    #先拉取之前的消息信息
    SEL = "SELECT  `MESSAGEBOX` FROM `badposts_user` WHERE `UID`=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    UPD = "UPDATE `badposts_user` SET `MESSAGEBOX`=\"" +  str(msgid) + "," + result[0][0] + "\" WHERE `UID`=\"" + uid + "\""
    print(UPD)
    DBCUR.execute(UPD)
    DBCONN.commit()  
    DBCUR.close()
    DBCONN.close()
    return True