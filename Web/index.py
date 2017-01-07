from flask import Flask
from flask import render_template,jsonify,redirect
from flask import request
import flask
import time
import worklib.getTeacherInfo as TI
import worklib.getInfoWeb as IW
import worklib.getnews as News
import worklib.subscrible as SUB
import bigdataQuery.checkmail as VerifyBigDataMail
import bigdataQuery.userFunctions as UserFunctions
import bigdataQuery.termgather as TG
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

#搜索指定词语的数据
@app.route('/tiebabigdata/term/<term>')
def showterm(term):
    status,data = TG.checkExistInTD(term)
    if status == True:  #已经被查询过，直接返回历史数据
        ID,TIMELINE,USERTABLESTR,COUNT =  TG.generateByResult(data)
        #return str(TIMELINE[0][0]) + "<hr/>" + str(TIMELINE[0][1])
        return render_template("wordsstatus.html",TERM=term,ATR="F",TBODY=USERTABLESTR,GDATA=TIMELINE[0][0],GDATAY=TIMELINE[0][1]);
    else:       #未被查询过，渲染模版，要求JS查询
        return render_template("wordsstatus.html",TERM=term,ATR="T",TBODY=HS.WORDSTATUS_TABLE_BODY,GDATA=['by','kanch'],GDATAY=[9,6]);
    return render_template('error.html')

#查看用户数据（经过邮箱验证后）
@app.route('/tiebabigdata/user/<sessiondata>/<xid>')
def bigdata_user(sessiondata,xid):
    veristatus = VerifyBigDataMail.checkSession(sessiondata)
    if veristatus == 1:
        info = UserFunctions.getBasicInfo(xid)
        if info[0] == False:
            return render_template('error.html')
        return render_template('tiebauser.html',xid=xid,session=sessiondata,TIEBAID=info[1],KEYWORD=info[10],TAGS=info[9],REALNAME=info[2],XUEHAO=info[3],GRADECLASS=info[8],QQ=info[4],EMAIL=info[6],PHONE=info[5])
    elif veristatus == -1:  #未查找到
        return render_template('error_verify.html',WHY="链接无效！<br/>您可能没有通过邮件验证！")
    elif veristatus == -2:  #过期
        return render_template('error_verify.html',WHY="链接已经过期！<br/>该链接已经过期，您需要重新验证以获取新的链接！<p>链接仅在24小时内有效！</p>")
    else:
        return render_template('error_verify.html',WHY="发生未知错误！")

#邮箱验证发送成功页面
@app.route('/verify/bigdata/success')
def bigdata_verifyMail_success():
    return render_template('verifyMailSent.html',MAIL="",NAME="")

#验证邮箱页面
@app.route('/verify/bigdata', methods=['POST'])
def bigdata_verifyMail():
    searchtarget = request.form['searchtarget']
    email = request.form['email']
    xid = 0
    status = UserFunctions.checkUser(searchtarget)
    if status == -1:
        xid = UserFunctions.insertIntoBigData(searchtarget)
        if xid == -1:
            return render_template('error.html')
    else:
        xid = status
    sig = VerifyBigDataMail.generateHash(email,searchtarget)
    VerifyBigDataMail.sendVerifyMail(email,sig,str(xid))
    return redirect('/verify/bigdata/success')

#转向该链接以启用邮箱验证
@app.route('/verify/bigdata/<searchtarget>')
def bigdata_verify_open(searchtarget):
    return render_template('requestVerifyMail.html',SEG=searchtarget)

#成信助手
@app.route('/newslist')
def newslist():
    return render_template("cuitnews.html")

@app.route('/getnews/<ntype>')
def getnews(ntype):
    #return News.getNews(ntype)
    return 'null'

@app.route('/subscrible/<email>/<stype>')
def sbuscrible(email,stype):
    return SUB.addToSubscribleList(email,stype)
    
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

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='10.105.91.217')
    #app.run(host='216.45.55.153')
    #app.run(host='127.0.0.1')
    app.run(host='127.0.0.1',debug=True)