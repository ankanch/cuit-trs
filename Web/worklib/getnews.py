import urllib.request


#用于获取正常新闻来自：http://www.cuit.edu.cn/NewsIndex1
def getNews(nsubname):
    url = "https://forcuit-151103.appsp0t.com/" + nsubname
    try:
        page = urllib.request.urlopen(url,timeout=58)
        html = page.read()
        return html
    except Exception as e:
        print("下载出错！重试中...",end="\t")
        return ""
    return ""

#用于获取国际交流处的新闻：通知公告
def getNews_Guoji_Tongzhi():
    pass