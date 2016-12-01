import smtplib 
from email.mime.text import MIMEText
from email.utils import formataddr
my_sender='kanchpybot@163.com' 
my_sender_password = "XYZ2016python"  

def SendMail(TO,TITLE,CONTENT):
    ret = Mail(TO,TITLE,CONTENT)
    if ret:
        print("Mail sent success!")
    else:
        print("Failed to sent mail!") 

def Mail(TO,TITLE,CONTENT):
  ret=True
  my_user = TO
  try:
    msg=MIMEText(CONTENT,'plain','utf-8')
    msg['From']=formataddr(["Kanch's PythonBot @ MyPythonVPS",my_sender])  
    msg['To']=formataddr(["Autosend by bot",my_user])
    msg['Subject']=TITLE 
 
    server=smtplib.SMTP("smtp.163.com",25) 
    server.login(my_sender,my_sender_password)  
    server.sendmail(my_sender,my_user,msg.as_string())  
    server.quit() 
  except Exception:  
    ret=False
  return ret
