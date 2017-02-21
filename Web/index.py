import time
import flask
from flask import Flask, jsonify, redirect, render_template, request
import badposts.badposts as BP
import badposts.vaildatecode as VC
import badposts.bpuser as BPUser
import bigdataQuery.checkmail as VerifyBigDataMail
import bigdataQuery.termgather as TG
import bigdataQuery.userFunctions as UserFunctions
import worklib.getInfoWeb as IW  
import worklib.getTeacherInfo as TI
import worklib.htmlstring as HS


app = Flask(__name__)

PATH_SEARCHCACHE = "/pyprojects/teacherRating/"
#FOR WEB VERSION
#FOR WEB VERSION
#FOR WEB VERSION
#FOR WEB VERSION
#成信助手首页 
@app.route('/')
def index():
    return render_template("index.html")

#老师评分系统
@app.route('/trs')
def hello():
    return render_template("search.html")

#成信贴吧大数据
@app.route('/tiebabigdata')
def bigdata():
    return render_template("bigdata.html")

#成信匿名墙-搜索
@app.route('/badborad/search/<tags>')
def searchbadposts(tags):
    result = BP.searchFor(tags)
    return BP.makeUpTable(result)

#成信匿名墙-时间线
@app.route('/badborad/')
@app.route('/badborad')
def badborad():
    return render_template("badborad.html",CURID=0)

#成信匿名墙-时间线-获取
@app.route('/badborad/load/<curid>/<qsum>')
def loadbp(qsum,curid):
    result,minid = BP.queryBadposts(qsum,curid)
    return minid + "<@BYKANCHOFCUITCSY@>" + BP.makeUpTable(result)

#成信匿名墙-具体页面
@app.route('/badborad/<int:xid>')
def showbadborad(xid):
    rl = BP.getBadposts(xid)
    return render_template("badpostsdetails.html",ID=rl[0],TITLE=rl[1],CONTENT=rl[2].replace("\n","<br/>"),DATE=rl[3],UP=rl[4], \
                            QUESTION=VC.getVaildateCode()[0],COMMENTSUM=BP.getCommentsSum(rl[0]))

#成信匿名墙-发布新曝光
@app.route('/badborad/newbad')
def postbadposts():
    return render_template("postNewBadposts.html",QUESTION=VC.getVaildateCode()[0])

#成信匿名墙-发布新曝光（POST）
@app.route('/badborad/submit', methods=['POST'])
def getbadborad():
    title = request.form['title']
    uid = request.form['uid']
    content = request.form['content']
    answer = request.form['a']
    question = request.form['q']
    if VC.check(question,str(answer)) == False:
        return "ERROR:v"
    xid = BP.insertBadposts(title,content,uid)
    return  str(xid)
    #return "22"

#成信匿名墙-支持曝光
@app.route('/badborad/up', methods=['POST'])
def supportbadborad():
    question = request.form['q']
    answer = request.form['a']
    xid = request.form['i']
    if VC.check(question,str(answer)) == False:
        return "ERROR:VC"
    if BP.support(xid) == False:
        return "ERROR:NB"
    return "O"

#成信匿名墙，发表回复
@app.route('/badborad/submitreply', methods=['POST'])
def postreply():
    rof = request.form['rof']
    uid = request.form['uid']
    rid = request.form["rid"]
    author = request.form['author']
    content = request.form['content']
    if  BP.insertReply(rof,uid,rid,author,content) == True:
        return "O"
    return  "F"

#成信匿名墙，加载回复
@app.route('/badborad/loadbrp/<rof>/<cursum>')
def loadbrp(rof,cursum):
    result,status = BP.queryReply(rof,cursum)
    return status + "<@BYKANCHOFCUITCSY@>" + BP.makeupReplyHtmlcode(result)

#成信匿名墙，自动注册新用户
@app.route('/badborad/user/newuser')
def autonewuser():
    return BPUser.generateUID()

#成信匿名墙，拉取指定用户的新消息数量
@app.route('/badborad/user/getmsg/<uid>')
def getusermsg(uid):
    return str(BPUser.getUnreadMsg(uid))

#成信匿名墙，拉取指定用户的昵称
@app.route('/badborad/user/getnickname/<uid>')
def getusernickname(uid):
    return str(BPUser.getUserNickname(uid))

#成信匿名墙，给定回复ID获取所在帖子
@app.route('/badborad/getrofbyrid/<rid>')
def getrofbyrid(rid):
    return str(BPUser.getrofbyrid(rid))

#成信匿名墙，更改指定用户的昵称
@app.route('/badborad/user/changenickname', methods=['POST'])
def changeusernickname():
    uid = request.form['u']
    nickname = request.form['n']
    BPUser.changeUserNickname(uid,nickname)
    return "O"

#成信匿名墙，用户消息中心
@app.route('/badborad/user/notifications/<uid>')
def notifications(uid):
    nickname = BPUser.getUserNickname(uid)
    return render_template("bpUserNitification.html",NICKNAME=nickname,UID=uid)

#成信匿名墙，拉取指定用户的消息内容列表
@app.route('/badborad/user/getmsgdetails/<uid>')
def getusermsgdetails(uid):
    unreadlist = BPUser.getUnreadMsgDetails(uid)
    return unreadlist

#成信匿名墙，清空未读消息列表
@app.route('/badborad/user/clearunread/<uid>')
def clearunreadmsg(uid):
    if BPUser.clearmsgbox(uid) == True:
        return "O"
    return "F"

#搜索指定词语的数据
@app.route('/tiebabigdata/term/<term>/<int:scale>')
@app.route('/tiebabigdata/term/<term>')
def showterm(term,scale=1):
    status,data = TG.checkExistInTD(term)
    if status == True:  #已经被查询过，直接返回历史数据
        ID,TIMELINE,USERTABLESTR,COUNT =  TG.generateByResult(data)
        #return str(TIMELINE[0][0]) + "<hr/>" + str(TIMELINE[0][1])
        TIMELINE = TG.ScaleData(TIMELINE,scale)
        return render_template("wordsstatus.html",TERM=term,ATR="F",TBODY=USERTABLESTR,GDATA=TIMELINE[0][0],GDATAY=TIMELINE[0][1],URL="/tiebabigdata/term/"+term)
    else:       #未被查询过，渲染模版，要求JS查询
        return render_template("wordsstatus.html",TERM=term,ATR="T",TBODY=HS.WORDSTATUS_TABLE_BODY,GDATA=['by','kanch'],GDATAY=[9,6],URL="/tiebabigdata/term/"+term)
    return render_template('error.html')

#查看用户数据
@app.route('/tiebabigdata/user/<xid>')
def bigdata_user(xid):
    info = UserFunctions.getBasicInfo(xid)
    RANDOM10 = UserFunctions.getRandom10Post(xid)
    if info[0] == False:
            return render_template('error.html')
    return render_template('tiebauser.html',RANDOM=RANDOM10,xid=xid,TIEBAID=info[1],KEYWORD=info[10],TAGS=info[9],REALNAME=info[2],XUEHAO=info[3],GRADECLASS=info[8],QQ=info[4],EMAIL=info[6],PHONE=info[5])

#不经过邮件验证，直接查询用户
@app.route('/tiebabigdata/bigdata/<searchtarget>')
def bigdata_noverify(searchtarget):
    xid = 0
    status = UserFunctions.checkUser(searchtarget)
    if status == -1:
        xid = UserFunctions.insertIntoBigData(searchtarget)
        if xid == -1:
            return render_template('error.html')
    else:
        xid = status
    return redirect('/tiebabigdata/user/'+ str(xid))


#老师评价系统
#老师评价系统
#老师评价系统
#老师评价系统
@app.route('/trs/filllostinfo/<int:id>')
def fillLostInfoWV(id):
    TIO = TI.getTeacherInfobyID(str(id))
    tid = str(TIO[0][0])
    name = TIO[0][1]
    subject = TIO[0][5]
    school = TIO[0][6]
    gender = str(TIO[0][7])
    return render_template("filllostinfo.html",NAME=name,SUBJECTS=subject,SCHOOL=school,TID=tid,GENDERVALUE=gender)

@app.route('/trs/autofill/<word>')
def autofill(word):
    return IW.autoFill(word)

@app.route('/trs/refreshld/<int:id>')
def refreshlikes(id):
    return IW.refreshLikes(id)

@app.route('/trs/getsearchtags')
def getSearchTages():
    return IW.getSearchTags()

@app.route('/trs/ranklist')
def showranklist():
    return render_template("ranklist.html")

@app.route('/trs/getranklist/<ltype>')
def getranklist(ltype):
    return IW.getRankList(ltype)

@app.route('/trs/adddislikeweb/<UID>/<int:id>')
def addwebdislike(UID,id):
    return IW.addOneUpWeb("DISLIKE",id,UID)

@app.route('/trs/addlikeweb/<UID>/<int:id>')
def addweblike(UID,id):
    return IW.addOneUpWeb("LIKE",id,UID)

@app.route('/trs/regmail/<mailaddr>')
def addmail(mailaddr):
    return IW.addMail(mailaddr)

@app.route('/trs/autoregiste')
def autoregiste():
    return IW.autoRegiste()  

@app.route('/trs/teacher/<name>')
def getTeacherInfoBynameWV(name):
    try:
        TIO = TI.getTeacherInfo(name)
        tid = str(TIO[0][0])
        name = TIO[0][1]
        subject = TIO[0][5]
        school = TIO[0][6]
        like = "(" + str(TIO[0][3]) + ")"
        dislike = "(" + str(TIO[0][4]) + ")"
        rating = TIO[0][2]
        gender = ""
        if str(TIO[0][7]) == "1":
            gender = "男"
        else:
            gender = "女"
    except Exception:
         return render_template("error.html")
    sum = TIO[0][3] + TIO[0][4]
    pxx = 0
    if sum != 0:
        pxx = TIO[0][3] / sum
        pxx *= 100
        round(pxx,2)
    f = open(PATH_SEARCHCACHE+"searchcache",'a')
    f.write(name+"\r\n")
    f.flush()
    f.close()
    return render_template("teacherinfo.html",NAME=name,SUBJECTS=subject,SCHOOL=school,GENDER=gender,LNUM=like,DLNUM=dislike,RATING=rating,TID=tid,LIKERATE=pxx)


@app.route('/trs/getcomments/<int:id>/<int:linestart>/')
def getComments(id,linestart):
    COMMENTSLIST =  TI.getComment(id,linestart,linestart+5)
    if COMMENTSLIST == "NULL":
        return "NULL"
    COMMENTSLIST = COMMENTSLIST.split("<br/>")
    COMMENTSBODY = ""
    for com in COMMENTSLIST:
        spf = com.replace(" ","")
        spf = spf.replace("\n","")
        spf = spf.replace("\r","")
        if(len(spf)>0):
            com = com.replace("CSYZL","<br/>")
            COMMENTSBODY = COMMENTSBODY + IW.COMMENTS_HEAD + com + IW.COMMENTS_TAIL
    return COMMENTSBODY

@app.route('/trs/getcommentssum/<int:id>/')
def getCommentsSum(id):
    return TI.getCommentSum(id)
@app.route('/trs/submitacomment', methods=['POST'])
def submitAComment():
    id = request.form['id']
    comment = request.form['comment']
    if comment.find("</a>") > -1 or comment.find("</script>") > -1 or comment.find("href") > -1:
        return "ERROR"
    return TI.addComment(int(id),comment)

@app.route('/trs/filllostinfo', methods=['POST'])
def fillLostInfo():
    id = request.form['id']
    subject = request.form['subject']
    school = request.form['school']
    gender = request.form['gender']
    print("Fill Info Recived:",id,subject,school,gender)
    return TI.fillLostInfo(id,subject,school,gender)
#FOR ANDROID APPLICATIONS
#FOR ANDROID APPLICATIONS
#FOR ANDROID APPLICATIONS
#FOR ANDROID APPLICATIONS
#FOR ANDROID APPLICATIONS

@app.route('/getinfo/<name>/')
def getinfo(name):
    STD = TI.getTeacherInfo(name)
    strd = ""
    for teacher in STD:
        strd = strd + str(teacher) +"<br/>"
    return strd

@app.route('/registeuser/<UID>/')
def registeUser(UID):
    return TI.registeUser(UID)

@app.route('/getratinglist/<UID>/')
def getRatingList(UID):
    return TI.getRatingList(UID)

@app.route('/getcomment/<int:id>/<int:linestart>/<int:lineend>/')
def getComment(id,linestart,lineend):
    return TI.getComment(id,linestart,lineend)



@app.route('/getinfo/<int:id>/')
def getinfobyID(id):
    STD = TI.getTeacherInfobyID(str(id))
    strd = ""
    for teacher in STD:
        strd = strd + str(teacher) +"<br/>"
    return strd

@app.route('/addlike/<UID>/<int:id>/')
def addlike(id,UID):
    return TI.addOneUp("LIKE",id,UID)

@app.route('/adddislike/<UID>/<int:id>/')
def adddislike(id,UID):
    return TI.addOneUp("DISLIKE",id,UID)

#错误页面定义
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='10.105.91.217')
    #app.run(host='127.0.0.1')
    app.run(host='127.0.0.1',debug=True)
