#coding:utf-8
import urllib

CUIT_SITE_PREFIX = "http://www.cuit.edu.cn/"
CUIT_GUOJICHU_SITE_PREFIX = "http://gjjl.cuit.edu.cn/info/"

def getHtml(url):
    page = urllib.request.urlopen(url,timeout=5)
    html = page.read().decode(errors='ignore')
    return html

#获取成信新闻的新闻
def getXueshuNews(html):
    NEWS_HEAD = "<div class=\"news1-page-content\">"
    NEWS_TAIL = "<div id=\"PageDiv\" class=\"page_div\">"
    html = html[html.find(NEWS_HEAD)+len(NEWS_HEAD):html.find(NEWS_TAIL)]
    html = html[html.find("</font>")+len("</font>"):]

    LINK_HEAD= "<a href='"
    LINK_TAIL = "' target="
    TITLE_HEAD = "target='_blank'>"
    TITLE_TAIL = "</a>"
    DATE_HEAD = "'datetime'>"
    DATE_TAIL = "</font>"
    
    news_list = ""
    while html.find(TITLE_HEAD) > -1:
        link = html[html.find(LINK_HEAD)+len(LINK_HEAD):html.find(LINK_TAIL)]
        html = html[html.find(LINK_HEAD)+len(LINK_HEAD):]
        title = html[html.find(TITLE_HEAD)+len(TITLE_HEAD):html.find(TITLE_TAIL)]
        html = html[html.find(TITLE_HEAD)+len(TITLE_HEAD):]
        date = html[html.find(DATE_HEAD)+len(DATE_HEAD):html.find(DATE_TAIL)]
        html = html[html.find(DATE_TAIL)+len(DATE_TAIL):]
        news_list = news_list + date + "<@>" + title + "<@>" + CUIT_SITE_PREFIX + link + "<br/>"
    return news_list

#获取国际交流处的通知公告
def getGuojijiaoliu(html):
    #寻找通知公告用的
    #用于国际交流
    TONGZHIGONGGAO_BEG = "leaderfont47665"
    TZGG_LINK_HEAD = "<a href=\"info/"
    TZGG_LINK_TAIL = "\" class="
    TZGG_TITLE_HEAD = "title=\""
    TZGG_TITLE_TAIL = "\" target="
    TONGZHIGONGGAO_END = "viewid=\"46836\""
    html = html[html.find(TONGZHIGONGGAO_BEG)+len(TONGZHIGONGGAO_BEG):html.find(TONGZHIGONGGAO_END)]
    TZGG_DATE_HEAD= "nowrap>"
    TZGG_DATE_END = "</td></tr>"
    
    news_list = ""
    while html.find(TZGG_TITLE_HEAD) > -1:
        link = html[html.find(TZGG_LINK_HEAD)+len(TZGG_LINK_HEAD):html.find(TZGG_LINK_TAIL)]
        html = html[html.find(TZGG_LINK_TAIL)+len(TZGG_LINK_TAIL):]
        title = html[html.find(TZGG_TITLE_HEAD)+len(TZGG_TITLE_HEAD):html.find(TZGG_TITLE_TAIL)]
        date = html[html.find(TZGG_DATE_HEAD)+len(TZGG_DATE_HEAD):html.find(TZGG_DATE_END)]
        html = html[html.find(TZGG_LINK_HEAD):]
        news_list = news_list + date + "<@>" + title + "<@>" + CUIT_GUOJICHU_SITE_PREFIX + link + "<br/>"
    return news_list

#获取校团委的活动预告
def getXiaoTuanWei_HuoDongYuGao(html):
    pass

#获取教务处的学科竞赛
def getXueKeJingSai():
    pass