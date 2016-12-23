"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from CUITHelperAPIX import app
from CUITHelperAPIX.NewsRetriver import zhuaqu as CUIT
from CUITHelperAPIX.NewsRetriver import MailService as MailService
from CUITHelperAPIX.NewsRetriver import cacheNews as NewsCache

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
#下面的都是学术动态，学术预告新闻
@app.route('/news_xueshu')
def news_xueshu():
    url_xueshu = "http://www.cuit.edu.cn/NewsList?id=4"
    return CUIT.getXueshuNews(CUIT.getHtml(url_xueshu))


