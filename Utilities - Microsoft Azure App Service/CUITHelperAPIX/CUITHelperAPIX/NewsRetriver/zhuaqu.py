#coding:utf-8
import urllib

CUIT_SITE_PREFIX = "http://www.cuit.edu.cn/"

def getHtml(url):
    page = urllib.request.urlopen(url,timeout=5)
    html = page.read().decode(errors='ignore')
    return html

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