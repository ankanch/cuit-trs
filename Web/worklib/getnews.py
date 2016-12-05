import urllib.request


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