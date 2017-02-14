#该脚本的作用是去除一些非法数据

#这个函数用来去除content里面的非法HTML标签
#目前我们只允许以下HTML标签：
#b,i,small,s,em
def cleanForbiddenHTMLElem(rawcontent):
    pass

#该函数的作用是读取content第4个\n之前的数据，然后在结尾加上......
def getAbstruct(rawcontent):
    if rawcontent.count('\n') >=4:
        p1 = rawcontent.find('\n')
        p2 = rawcontent.find('\n',p1+1)
        p3 = rawcontent.find('\n',p2+1)
        adstr = rawcontent[:rawcontent.find('\n',p3+1)-1] + "......"
        return adstr
    if len(rawcontent) > 333:
        return rawcontent[0:333]+"......"
    return rawcontent