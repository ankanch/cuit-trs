#coding:utf-8
import logging

from flask import Flask
from flask import render_template
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import cuitzhuaqu.zhuaqu as CUIT
import cuitzhuaqu.MailService as MailService
import cuitzhuaqu.cacheNews as NewsCache


app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
def hello():
    return render_template("index.html",INFO="...")

@app.route('/newslist')
def newslist():
    return render_template("newslist.html")

#下面的都是学术动态，学术预告新闻
@app.route('/news_xueshu')
@crossdomain(origin='*')
def news_xueshu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_xueshu")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_xueshu_update')
def news_xueshu_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_xueshu")
    NewsCache.refreshCache(newslistdata,"news_xueshu") #刷新新闻缓存
    return update_news

#下面的都是文化活动，学生社团活动
@app.route('/news_wenghua')
@crossdomain(origin='*')
def news_wenghua():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=10"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_wenghua")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_wenghua_update')
def news_wenghua_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=10"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_wenghua")
    NewsCache.refreshCache(newslistdata,"news_wenghua") #刷新新闻缓存
    return update_news

#下面的都是信息公告
@app.route('/news_xingxigonggao')
@crossdomain(origin='*')
def news_xingxigonggao():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=2"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_xingxigonggao")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_xingxigonggao_update')
def news_xingxigonggao_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=2"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_xingxigonggao")
    NewsCache.refreshCache(newslistdata,"news_xingxigonggao") #刷新新闻缓存
    return update_news

#下面的都是焦点新闻
@app.route('/news_jiaodian')
@crossdomain(origin='*')
def news_jiaodian():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=3"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_jiaodian")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_jiaodian_update')
def news_jiaodian_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=3"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_jiaodian")
    NewsCache.refreshCache(newslistdata,"news_jiaodian") #刷新新闻缓存
    return update_news

#下面的都是工作交流
@app.route('/news_gongzuojiaoliu')
@crossdomain(origin='*')
def news_gongzuojiaoliu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=5"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_gongzuojiaoliu")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_gongzuojiaoliu_update')
def news_gongzuojiaoliu_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=5"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_gongzuojiaoliu")
    NewsCache.refreshCache(newslistdata,"news_gongzuojiaoliu") #刷新新闻缓存
    return update_news

#下面的都是综合新闻
@app.route('/news_zonghe')
@crossdomain(origin='*')
def news_zonghe():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    #newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    #cachecoee = NewsCache.refreshCache(newslistdata,"news_zonghe")
    #return cachecoee  + newslistdata
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_zonghe_update')
def news_zonghe_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_zonghe")
    NewsCache.refreshCache(newslistdata,"news_zonghe") #刷新新闻缓存
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
