#coding=utf-8

import MailService
import os
import threading
import urllib.request as Request
import datetime
import time

#这个脚本用来定时从https://forcuit-151103.appspot.com/news_xueshu_update 获取我们学校学术预告的更新新闻的
CHECK_PER_SECONDS = 29*60

def getXueshuNewsUpdate():
    now = datetime.datetime.now()
    timestr = now.strftime('%Y-%m-%d %H:%M:%S')  
    print(timestr + ":  CUIT->start check news update...")
    url = "https://forcuit-151103.appspot.com/news_xueshu_update"
    page = Request.urlopen(url)
    data = page.read().decode("utf-8","igonre")
    if data=="NO UPDATE YET":
        print("\tCUIT:XueshuNews->no update yet")
        return "N"
    else:
        updatelist = data.split("<br/>")
        newscontent = ""
        for news in updatelist:
            if len(news) < 5:
                continue
            news = news.split("<@>")
            href = "\t<p><a href=\"" + news[2] + "\"target=\"_blank\">" + news[1] + news[0] + "</a></p>"
            newscontent+=href
        data = "有新的学术预告！\r\n\r\n" + newscontent + "\r\n\r\n\r\n**你之所以会收到该邮件，是因为你已经订阅成都信息工程大学学术预告新闻更新。"
        MailService.SendMail("1075900121@qq.com","成都信息工程大学->新【学术预告】",data)
        print("\tCUIT:XueshuNews->news update!")
        Request.urlopen("https://forcuit-151103.appspot.com/news_xueshu").read()
        return "Y"


print("CUIT Auto News Retriver started!\n\tCtrl + C to stop")
print("Application will check every",CHECK_PER_SECONDS/60,"minutes.\n\n")
getXueshuNewsUpdate()
while True:
    time.sleep(CHECK_PER_SECONDS)
    getXueshuNewsUpdate()