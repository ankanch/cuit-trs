import pymysql as SQL
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
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "INSERT INTO `bigdata_verify_mail`( `SHA1`, `EMAIL`, `TARGET`, `TIMETICK`, `VERIFIED`, `OUTOFDATE`) VALUES ("
    INS = INS + "\"" + sha1 +"\",\"" + email +"\",\"" + searchtarget +"\"," + str(timeticks) + ",False ,False)"
    DBCUR.execute("SET names 'utf8mb4'")
    DBCUR.execute(INS)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    #返回生成的hash
    return sha1


#向用户邮箱发送验证邮件
def sendVerifyMail(email,hashdata,target):
    CONTENT = """
    你好，你在成信贴吧大数据查询的"""+ target +"""的资料页面如下，请在24小时内点击下列链接查看。"""
    hashurl = "http://cuithelperapix.azurewebsites.net/verify/bigdata/" + hashdata + "/" + target
    CONTENT += "<a href=\""+ hashurl +"\" target=\"_blank\">"+ hashurl + "</a>"
    CONTENT+= "<br/><br/>您之所以会收到该邮件是因为您最近在 成信贴吧大数据（http://cuit.akakanch.com） 进行了查询。"
    sender = 
    senderpass = 
    if MailService.MailTo(email,"成信助手贴吧大数据查询邮箱验证",CONTENT,sender,senderpass) == True:
        return True
    return False

#该函数用来检测session是否正确
#超过24小时，就返回错误
#session未验证返回错误
def checkSession(sessiondata):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
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
