from bs4 import BeautifulSoup
import re

#应该分为两部分：爬取帖子列表的，和爬取帖子内容的


#@该函数用来去除指定字符串中的所有HTML标签
#@返回值（str）:去除HTML标签后的字符串
def clearHTML(raw):
    htmlcleanr = re.compile('<.*?>')
    cleantext = re.sub(htmlcleanr, '', raw)
    return cleantext


#@该函数用来获取当前页面的所有回帖数据(未格式化，还存在html标签)
#@返回值（list）,str：[  [发帖用户,回帖信息,发帖时间,REPLY_TO], [发帖用户,回帖信息,发帖时间,REPLY_TO],... ]和楼主
def getReplyList(html,firstfloor="NULL",clearhtml=True):
    soup = BeautifulSoup(html,"html.parser")
    replylist_html = soup.select("#j_p_postlist div[data-field]")
    result = []
    for replyblock in replylist_html:
        author = replyblock.find("a",class_="j_user_card")
        if author == None:
            #跳过空数据
            continue
        #匹配发帖人
        try:#.contents[0] 可能不存在
            postauthor = author.contents[0]
        except Exception as e:
            continue
        #匹配内容（未格式化）
        postcontent = replyblock.find("div",class_="j_d_post_content")
        if clearhtml == True:
            #是否格式化数据
            postcontent = postcontent.text
        else:
            postcontent = str(postcontent)
            print(postcontent)
        #匹配时间
        data_field = replyblock["data-field"]
        postdate = data_field[data_field.find("2",data_field.find("date")):data_field.find("vote_crypt")-3]
        #匹配楼层
        post_no = data_field[data_field.find(":",data_field.find("post_no"))+1:data_field.find(",",data_field.find("post_no"))]
        #设置楼主，方便设置replyto数据域
        if int(post_no) == 1:
            firstfloor = postauthor
        #print(post_no,postdate,postauthor)
        result.append([postauthor,postcontent,postdate,firstfloor])
    return result,firstfloor


#@该函数用来获取当前页面的所有帖子列表
#@返回值（list）：[  [帖子标题，链接，发帖人],[帖子标题，链接，发帖人],... ]
def getPostsList(html):
    soup = BeautifulSoup(html,"html.parser")
    postlist_html = soup.select("#thread_list li[data-field] div.threadlist_title a[href]")
    result = []
    for posttitle in postlist_html:
        postd = [posttitle['title'],posttitle['href']]
        #print(postd)
        result.append(postd)
    return result


#@该函数用来获取所有的楼中楼回复，传入 bs4.element.tag对象
#@返回值（list）:[  [发帖用户,回帖信息,发帖时间,REPLY_TO], [发帖用户,回帖信息,发帖时间,REPLY_TO],... ]
#此处的reply为楼主
def getInterReply(replyblock,clearhtml=True):
    interreplylist = replyblock.find("div",class_="j_lzl_c_b_a core_reply_content")