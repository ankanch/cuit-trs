#coding:utf-8  
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
my_sender= #发件人邮箱账号，为了后面易于维护，所以写成了变量
my_sender_password =   #发件人邮箱

#请调用该函数发送邮件
def SendMail(TO,TITLE,CONTENT):
    ret = Mail(TO,TITLE,CONTENT)
    if ret:
        print("Mail sent success!") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
    else:
        print("Failed to sent mail!") #如果发送失败则会返回filed

def Mail(TO,TITLE,CONTENT):
  ret=True
  my_user = TO
  msg=MIMEText(CONTENT,'plain','utf-8')
  msg['From']=formataddr(["成信助手 CUIT Helper",my_sender])  
  msg['To']=formataddr(["Subscriber",my_user])
  msg['Subject']="no-reply:" + TITLE + "\t成信助手 | CUIT Helper" #邮件的主题
  try:
    server=smtplib.SMTP_SSL("smtp.exmail.qq.com",465) 
    server.login(my_sender,my_sender_password) 
    server.sendmail(my_sender,my_user,msg.as_string()) 
    server.quit() 
  except Exception:  
    ret=False
  return ret

def MailTo(TO,TITLE,CONTENT,sender,senderpass):
  ret=True
  my_user = TO
  msg=MIMEText(CONTENT,'html','utf-8')
  msg['From']=formataddr(["成信助手 CUIT Helper",sender])  
  msg['To']=formataddr(["Subscriber",my_user])
  msg['Subject']="no-reply:" + TITLE + "\t成信助手 | CUIT Helper" #邮件的主题
  try:
    server=smtplib.SMTP_SSL("smtp.exmail.qq.com",465) 
    server.login(sender,senderpass) 
    server.sendmail(sender,my_user,msg.as_string()) 
    server.quit() 
  except Exception:  
    ret=False
  return ret
 
#SendMail("1075900121@qq.com",'测试邮件','括号中对应的是发件人邮箱账号、括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件邮箱密码')
