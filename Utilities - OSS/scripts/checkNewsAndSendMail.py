#coding=utf-8
import pymysql
import module.MailService as MailService
import os
import threading
import urllib.request as Request
import module.datebase as DB
import datetime
import time

#这个脚本用来检测是否有新闻更新，然后再给相应的订户发送提醒邮件
#新闻API接口列表 ：“新闻源名称”，“数据库字段名”，“API接口地址”
NEWS_LIST = [["XueshuNewss","N1","http://forcuit-151103.appspot.com/news_xueshu_update"],   #学术新闻
             ["ZongheNews","N3","http://forcuit-151103.appspot.com/news_zonghe_update"],         #综合新闻
             ["WenghuaHuoDong","N2","http://forcuit-151103.appspot.com/news_wenghua_update"],    #文化活动
             ["XingxiGonGao","N5","http://forcuit-151103.appspot.com/news_xingxigonggao_update"], #信息公告
             ["GongZuoJiaoLiu","N6","http://forcuit-151103.appspot.com/news_gongzuojiaoliu_update"],   #工作交流
             ["JiaoDianXinWeng","N4","http://forcuit-151103.appspot.com/news_jiaodian_update"],      #焦点新闻
            ]

#新闻检测函数
def checkNews(url,DBSEC):
    page = Request.urlopen(url)
    data = page.read().decode("utf-8","igonre")
    if data=="NO UPDATE YET":
        print("\t\t\t\t|->->no update yet")
        return 
    else:
        updatelist = data.split("<br/>")
        newscontent = ""
        for news in updatelist:
            if len(news) < 5:
                continue
            news = news.split("<@>")
            href = "\t<p><a href=\"" + news[2] + "\"target=\"_blank\">" + news[1] + news[0] + "</a></p>"
            newscontent+=href
        print("\t\t\t\t|->->news update!")
        ##发送通知邮件
        NotifySubscribler(DBSEC,newscontent)

#批量发送邮件函数
def NotifySubscribler(DBSEC,newscontent):
    print("\t\t\t\t|->->->gathering scbscribler info...")
    DBCONN = pymysql.connect(host=DB.DBL_CONNECTION_HOST_CH, port=3306,user=DB.DBL_CONNECTION_USER_CH,passwd=DB.DBL_CONNECTION_PASSWORLD_CH,db=DB.DBL_CONNECTION_DATABASE_NAME_CH,charset='UTF8')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT EMAIL FROM `news_subscribler` WHERE " + DBSEC +"=\"1\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    emaildata = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    emaillist = []
    for sucrib in emaildata:
        emaillist.append(sucrib[0])
    #print(emaillist)
    print("\t\t\t\t|->->->sending notify to",len(emaillist),"subscriblers.")
    data = "有新的学术预告！\r\n\r\n" + newscontent + "\r\n\r\n\r\n**你之所以会收到该邮件，是因为你已经订阅成都信息工程大学学术预告新闻更新。"
    MailService.SendMail(emaillist,"成都信息工程大学->新【学术预告】",data,"\t\t\t\t|->->->")

###################################################################################################
#####程序逻辑
###################################################################################################
print("\t\t|->CUIT Auto News Retriver started!")
now = datetime.datetime.now()
timestr = now.strftime('%Y-%m-%d %H:%M:%S')  
print("\t\t|->CUIT->start check news update...")
for newsurl in NEWS_LIST:
    print("\t\t\t|->Start check",newsurl[0],"...")
    checkNews(newsurl[2],newsurl[1])
print("\t\t|->News Check Finished!")