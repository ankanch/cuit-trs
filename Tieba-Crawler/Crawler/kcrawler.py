import urllib.request


#该函数用于编码网址和它的参数（包含中文的时候）
def urlEncode(raw_url,paras):
    KWD = urllib.parse.urlencode(paras)
    URL = raw_url + KWD 
    return URL

#用于下载网页，遇到错误重新尝试，直到下载成功
def getHtml(url):
    while True:
        try:
            page = urllib.request.urlopen(url,timeout=5)
            html = page.read()
            return html
        except Exception as e:
            print(".",end="")

