"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,redirect
from flask_json  import FlaskJSON, JsonError, json_response, as_json
from CUITHelperAPIX import app
from CUITHelperAPIX.NewsRetriver import zhuaqu as CUIT
from CUITHelperAPIX.NewsRetriver import MailService as MailService
from CUITHelperAPIX.NewsRetriver import cacheNews as NewsCache
from CUITHelperAPIX.QueryAPI import verifyMail as VerifyMail
from CUITHelperAPIX.QueryAPI import BigDataQueryAPI as QueryAPI
from CUITHelperAPIX.QueryAPI import termanalyze as TermAnalyze

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
    )

@app.route('/howto')
def howto():
    return "这是一个测试页面，显示API的用法"
############################333
#       下面是单词数据查询接口
############################333
#获取一个单词的发帖量最高的前10位用户和单词的时间线
@app.route('/api/tiebabigdata/wordstatisc/<word>')
def api_statisword(word):
    if TermAnalyze.checkExist(word) == True:
        return "错误！数据已经存在！"
    usercount,timeline = TermAnalyze.statisANDTimeline(TermAnalyze.searchForInclude(word))
    tstr,ustr = TermAnalyze.slice(usercount,timeline)
    TermAnalyze.saveToDB(ustr,tstr,word)
    return ustr+"<hr/>"+tstr
############################333
#       下面是用户数据查询接口
############################333
#获取用户的累计发帖量和最近30天发帖数据
@app.route('/api/tiebabigdata/postsum/<int:xid>')
@app.route('/api/tiebabigdata/postsum/<session>/<int:xid>')
def api_postsum(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    count,count30 = QueryAPI.getTotalPostsSum(xid)
    return str(count) + "," + str(count30)

#获取活跃时间段图数据
@app.route('/api/tiebabigdata/activitytimezon/<int:xid>')
@app.route('/api/tiebabigdata/activitytimezon/<session>/<int:xid>')
def api_activitytimezone(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getActivityTimeZone(xid)
    return str(listt)


#获取最近活跃度图
@app.route('/api/tiebabigdata/activitytimeline/<int:xid>/<int:days>')
@app.route('/api/tiebabigdata/activitytimeline/<session>/<int:xid>/<int:days>')
def api_activitytimeline(xid,days,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getActivityTimeLine(xid,days)
    return str(listt)

#获取用户关系图数据
@app.route('/api/tiebabigdata/relationcircle/<int:xid>')
@app.route('/api/tiebabigdata/relationcircle/<session>/<int:xid>')
@as_json
def api_relationcircle(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getReadlationCircle(xid)
    i=0
    iljson = []
    for v in listt[1]:
        iljson.append([dict(name=listt[0][i],values=v)])
        i+=1
    ditt = {}
    return dict(label=listt[0],value=iljson)

#获取常用关键字图
@app.route('/api/tiebabigdata/keymap/<int:xid>')
@app.route('/api/tiebabigdata/keymap/<session>/<int:xid>')
def api_keymap(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    listt =  QueryAPI.getKeymap(xid)
    return str(listt)

#获取用户标签
@app.route('/api/tiebabigdata/gettags/<int:xid>')
@app.route('/api/tiebabigdata/gettags/<session>/<int:xid>')
def api_gettags(xid,session=""):
    if session != "":
        if QueryAPI.checkSession(session) == False:
            return  "会话无效或已经过期！"
    return "这是一个测试页面，显示API的用法"
############################333
#       下面是邮箱验证接口
############################333
@app.route('/verify/bigdata/<hashdata>/<searchtarget>')
def mailcheck(hashdata,searchtarget):
    status = VerifyMail.checkHash(hashdata)
    if status == 1: #成功验证
        return redirect('http://cuit.akakanch.com/tiebabigdata/user/' + hashdata + "/" + searchtarget)
    elif status == -2: #过期
        return '链接已经过期！你需要重新验证！'
    elif status == -1: #无效
        return "无效链接！"
    else:
        return "发生未知错误，请联系 kanch@akakanch.com"


############################333
#       下面的都是新闻
############################333
@app.route('/jwc_xuekejingsai')
def JWC_XueKeJinSai():
    url = "http://jwc.cuit.edu.cn/Information/L3NewsList/c382c5627c6943c5916c77d9ae8d6c15/1"
    return CUIT.getXueKeJingSai(CUIT.getHtml(url))

@app.route('/jwc_xuekejingsai_update')
def JWC_XueKeJinSai_update():
    url = "http://jwc.cuit.edu.cn/Information/L3NewsList/c382c5627c6943c5916c77d9ae8d6c15/1"
    newslistdata = CUIT.getXueKeJingSai(CUIT.getHtml(url))
    update_news = NewsCache.checkNewNews(newslistdata,"jwc_xuekejingsai")
    NewsCache.refreshCache(newslistdata,"jwc_xuekejingsai") #刷新新闻缓存
    return update_news

@app.route('/huodongyugao')
def XTWHuoDongYUGao():
    url_guojijiaoliu = "http://xtw.cuit.edu.cn/a/huodongyugao/"
    return CUIT.getXiaoTuanWei_HuoDongYuGao(CUIT.getHtml(url_guojijiaoliu))

@app.route('/huodongyugao_update')
def XTWHuoDongYUGao_update():
    url = "http://xtw.cuit.edu.cn/a/huodongyugao/"
    newslistdata = CUIT.getXiaoTuanWei_HuoDongYuGao(CUIT.getHtml(url))
    update_news = NewsCache.checkNewNews(newslistdata,"huodongyugao")
    NewsCache.refreshCache(newslistdata,"huodongyugao") #刷新新闻缓存
    return update_news

@app.route('/guojijiaoliu')
def guojijiaoliu():
    url_guojijiaoliu = "http://gjjl.cuit.edu.cn/"
    return CUIT.getGuojijiaoliu(CUIT.getHtml(url_guojijiaoliu))

@app.route('/guojijiaoliu_update')
def guojijiaoliu_update():
    url_guojijiaoliu = "http://gjjl.cuit.edu.cn/"
    newslistdata = CUIT.getGuojijiaoliu(CUIT.getHtml(url_guojijiaoliu))
    update_news = NewsCache.checkNewNews(newslistdata,"guojijiaoliu")
    NewsCache.refreshCache(newslistdata,"guojijiaoliu") #刷新新闻缓存
    return update_news

@app.route('/newslist')
def newslist():
    return render_template("newslist.html")
#下面的都是学术动态，学术预告新闻
@app.route('/news_xueshu')
def news_xueshu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
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
def news_wenghua():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=10"
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
def news_xingxigonggao():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=2"
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
def news_jiaodian():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=3"
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
def news_gongzuojiaoliu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=5"
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
def news_zonghe():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))

@app.route('/news_zonghe_update')
def news_zonghe_update():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=1"
    newslistdata = CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))
    update_news = NewsCache.checkNewNews(newslistdata,"news_zonghe")
    NewsCache.refreshCache(newslistdata,"news_zonghe") #刷新新闻缓存
    return update_news


