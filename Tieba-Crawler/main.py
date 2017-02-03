import Parser.kparser as Parser
import Crawler.kcrawler as Crawler

BEGIN_PAGE = "http://tieba.baidu.com/f?kw="
POST_SUFFIX = "http://tieba.baidu.com"

plist = Crawler.getHtml(Crawler.urlEncode(BEGIN_PAGE,{'kw':"成都信息工程大学"}))
postlist = Parser.getPostsList(plist)
print(len(postlist))
tiezi = Crawler.getHtml(POST_SUFFIX + postlist[0][1])
replylist,louzu  = Parser.getReplyList(tiezi)
print(len(replylist))
for x in replylist:
    print(x)