from flask import Flask
from flask import render_template,jsonify
from flask import request
import flask
import time
import worklib.getTeacherInfo as TI
import worklib.getInfoWeb as IW
import worklib.getnews as News
import worklib.subscrible as SUB
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
    app.run(host='127.0.0.1')