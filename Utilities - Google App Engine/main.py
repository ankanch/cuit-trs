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

@app.route('/newslist')
def newslist():
    return render_template("newslist.html")

#下面的都是学术动态，学术预告新闻
@app.route('/news_xueshu')
def news_xueshu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_xueshu")
    return cachecoee  + newslistdata

@app.route('/news_xueshu_update')
def news_xueshu_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_xueshu")
    return update_news

#下面的都是文化活动，学生社团活动
@app.route('/news_wenghua')
def news_wenghua():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=10"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_wenghua")
    return cachecoee  + newslistdata

@app.route('/news_wenghua_update')
def news_wenghua_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=10"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_wenghua")
    return update_news

#下面的都是信息公告
@app.route('/news_xingxigonggao')
def news_xingxigonggao():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=2"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_xingxigonggao")
    return cachecoee  + newslistdata

@app.route('/news_xingxigonggao_update')
def news_xingxigonggao_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=2"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_xingxigonggao")
    return update_news

#下面的都是焦点新闻
@app.route('/news_jiaodian')
def news_jiaodian():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=3"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_jiaodian")
    return cachecoee  + newslistdata

@app.route('/news_jiaodian_update')
def news_jiaodian_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=3"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_jiaodian")
    return update_news

#下面的都是工作交流
@app.route('/news_gongzuojiaoliu')
def news_gongzuojiaoliu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=5"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_gongzuojiaoliu")
    return cachecoee  + newslistdata

@app.route('/news_gongzuojiaoliu_update')
def news_gongzuojiaoliu_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=5"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_gongzuojiaoliu")
    return update_news

#下面的都是综合新闻
@app.route('/news_zonghe')
def news_zonghe():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    cachecoee = NewsCache.refreshCache(newslistdata,"news_zonghe")
    return cachecoee  + newslistdata

@app.route('/news_zonghe_update')
def news_zonghe_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_zonghe")
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
