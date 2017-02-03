import Parser.kparser as Parser
import Crawler.kcrawler as Crawler
import config.urls as URL

BEGIN_PAGE =  URL.POST_LIST_SUFFIX
POST_SUFFIX = URL.POST_SUFFIX

plist = Crawler.getHtml(Crawler.urlEncode(BEGIN_PAGE,{'kw':"成都信息工程大学"}))
print(Crawler.getTiebaPageSum(plist))
postlist = Parser.getPostsList(plist)
print(len(postlist))
tiezi = Crawler.getHtml(POST_SUFFIX + postlist[0][1])
replylist,louzu  = Parser.getReplyList(tiezi)
print(len(replylist))

Crawler.downloadPost(POST_SUFFIX + postlist[0][1])
i=1
for post in postlist:
    hbuf = Crawler.getHtml(POST_SUFFIX+post[1])
    print(Crawler.getPostPages(hbuf),"-",i,end="\t")
    i+=1