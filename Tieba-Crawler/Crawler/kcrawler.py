import urllib.request
import Crawler.cachedata as Cache
import config.urls as URL


#该函数用于编码网址和它的参数（包含中文的时候）
def urlEncode(raw_url,paras):
    KWD = urllib.parse.urlencode(paras)
    URL = raw_url + KWD 
    return URL

#用于下载网页，遇到错误重新尝试，直到下载成功
def getHtml(url):
    #print(url)
    while False:
        try:
            page = urllib.request.urlopen(url,timeout=5)
            html = page.read()
            return html
        except Exception as e:
            print(".",end="")
    page = urllib.request.urlopen(url,timeout=5)
    html = page.read()
    return html

#该函数用于找出该帖子有多少页的回复
#如果返回 1 则表示只有1页
def getPostPages(html):
    html = html.decode('UTF-8','ignore')
    panchor = html.find("\">尾页</a>")
    ppp = html.find(">下一页</a>")
    pages = html[html.find("/p/",ppp):panchor]
    pages = pages[pages.find("=")+1:]
    if pages == "":
        return 1
    return int(pages)

#该函数用来完整的下载一个帖子（传入帖子第一页的url）
#返回下载的帖子的html
def downloadPost(url):
    #第一页需要单独处理，为了获取帖子有多少页
    hd = getHtml(url)
    #得到帖子页数
    pages = getPostPages(hd)
    #首先缓存第一页数据，方便后续处理
    filenamesuffix = url.replace(URL.POST_SUFFIX,"").replace("/","") + "-"
    Cache.saveToCache(hd,filenamesuffix+"1")
    if pages == 1:
        return 1
    page = pages
    while pages != 1:
        hd = getHtml(url + URL.POST_PARAMS + str(pages))
        Cache.saveToCache(hd,filenamesuffix+str(pages))
        pages-=1
    return page



#寻找贴吧总共有多少页,传入首页html
#返回总页数，这些页数应该是50的倍数
def getTiebaPageSum(html):
    html = html.decode('UTF-8','ignore')
    panchor = html.find(">尾页</a>")
    ppp = html.find(">下一页&gt;</a>")
    pages = html[html.find("&pn",ppp):panchor]
    pages = pages[pages.find("=")+1:pages.find("\"")]
    return int(pages)