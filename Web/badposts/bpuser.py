import datasourceconfig.database_settings as DBS
import badposts.badposts as BP
import pymysql as SQL
import random
import string
import time

#该脚本处理匿名墙用户相关内容

def generate():
    x = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    x += ''.join(random.sample(string.ascii_letters+string.digits, 16))
    x += str(time.time()) #加上时间戳，这样重复几率非常小
    return  x

#生成用户ID并插入数据库（已查重）
#返回值：用户iD
def generateUID():
    uid = generate()
    #db
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    #首先数据库查重
    SEL = "SELECT ID FROM `badposts_user` WHERE UID=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    print(result)
    if len(result) != 0:
        #发现ID重复，第二次生成重复ID的几率极低，故不再检查
        uid = generate()
    #插入数据库
    SEL = "INSERT INTO `badposts_user`(`NICKNAMES`, `MESSAGEBOX`, `UID`) VALUES (\"匿名用户\",\"@\",\"" + uid + "\")"
    DBCUR.execute(SEL)
    DBCONN.commit()
    #关闭链接
    DBCUR.close()
    DBCONN.close()
    return uid


#查询一个用户是否有未读消息
#返回值未读消息数量
#一个逗号即一个回复，因为储存格式为1，2，3，
def getUnreadMsg(uid):
    count = 0
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT MESSAGEBOX FROM `badposts_user` WHERE UID=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()[0][0]
    #result: unread @ 已读
    result = result.split("@")[0]
    count = result.count(',')
    #print(result)
    DBCUR.close()
    DBCONN.close()
    return count

#查询一个用户的昵称
def getUserNickname(uid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT NICKNAMES FROM `badposts_user` WHERE UID=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()[0][0]
    #result: unread @ 已读
    print(result)
    DBCUR.close()
    DBCONN.close()
    return result


#修改一个用户的昵称
def changeUserNickname(uid,nickname):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "UPDATE `badposts_user` SET NICKNAMES=\"" + nickname + "\" WHERE UID=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    return True


#返回用户的所有未读消息内容
#返回值，所有未读消息list
def getUnreadMsgDetails(uid):
    #首先要拿到消息列表
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT MESSAGEBOX FROM `badposts_user` WHERE UID=\"" + uid + "\""
    print(SEL)
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    #result: unread @ 已读
    result = result[0][0].split("@")[0]
    if result == "" or len(result)<2 :
        return "NULL"
    result = result[:len(result)-1]
    #result = result.split(',')
    #print(result)
    DBCUR.close()
    DBCONN.close()
    #接下来从另外一个表中读取满足条件的回帖
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `badposts_reply` WHERE ID in(" + result + ")"
    print(SEL)
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    #print(result)
    DBCUR.close()
    DBCONN.close()
    #返回数据
    return BP.makeupReplyHtmlcode(result)

#给定回复ID，用于获取该回复所在主题匿名贴地址
#传入回复ID
def getrofbyrid(replyid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT ROF FROM `badposts_reply` WHERE ID=" + replyid 
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()[0][0]
    print(result)
    DBCUR.close()
    DBCONN.close()
    return result

#清空一个用户的消息列表
def clearmsgbox(uid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT MESSAGEBOX FROM `badposts_user` WHERE UID=\"" + uid + "\"" 
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()[0][0]
    print(result)
    result = result.split("@")
    pr = "@" + result[1] + result[0]
    SEL = "UPDATE `badposts_user` SET `MESSAGEBOX`=\"" + pr + "\" WHERE `UID`=\"" + uid + "\"" 
    print(SEL)
    DBCUR.execute(SEL)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    return True

#该函数用来检测指定用户ID是否存在
def verifyUser(uid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `badposts_user` WHERE UID=\"" + uid + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return False
    return True
