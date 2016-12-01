#coding:utf-8
import logging

from flask import Flask
from flask import render_template
import cuitzhuaqu.zhuaqu as CUIT
import cuitzhuaqu.MailService as MailService
import cuitzhuaqu.cacheNews as NewsCache


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html",INFO="...")

@app.route('/news_xueshu')
def news_xueshu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata)
    return cachecoee  + newslistdata

@app.route('/news_xueshu_update')
def news_xueshu_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata)
    return update_news

@app.route('/mailtest')
def mailtest():
    return MailService.SendMail("1075900121@qq.com","TEST from GAE","Google App Enigne")

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.<br/>please contact kanch@akakanch.com')
    return 'An internal error occurred.<br/>please contact kanch@akakanch.com', 500
# [END app]
