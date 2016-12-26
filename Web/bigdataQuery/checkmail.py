import pymysql
import hashlib
import time 
import worklib.MailService as MailService
import datasourceconfig.database_settings as DBS
import datasourceconfig.mail_account as MAIL

#这个库用来生成验证码并插入数据库，然后发送邮件验证

#根据输入的邮箱和搜索目标生成验证Hash
def generateHash(email,searchtarget):
    #获取时间戳
    timeticks = time.time();
    #根据emai和searchtaeget生成hash
    data = hashlib.sha1()
    data.update((email+searchtarget).encode('utf-8'))
    sha1 = data.hexdigest()
    #将生成的3者插入数据库
    #DBCONN = SQL.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    #DBCONN.set_charset('utf8mb4')
    #DBCUR = DBCONN.cursor()
    INS = ""
    #DBCUR.execute("SET names 'utf8mb4'")
    #DBCUR.execut(INS)
    #DBCUR.commit()
    #DBCUR.close()
    #DBCONN.close()
    #返回生成的hash
    return sha1


#向用户邮箱发送验证邮件
def sendVerifyMail(email,hashdata):
    CONTENT = ""
    hashurl = "" + hashdata
    sender = ""
    senderpass = ""
    if MailService.MailTo(email,"成信助手贴吧大数据查询邮箱验证",CONTENT,sender,snederpass) == True:
        return True
    return False

#该函数用来检测session是否正确
#超过24小时，就返回错误
#session未验证返回错误
def checkSession(sessiondata):
    #获取时间戳
    timeticks = time.time();
    DBCONN = SQL.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = ""
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execut(SEL)
    DBCUR.commit()
    DBCUR.close()
    DBCONN.close()
