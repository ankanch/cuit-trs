import pymysql
import linecache
import random
from flask import jsonify
import worklib.getTeacherInfo as TI
import worklib.database as DBL
import worklib.htmlstring as HS

#数据库相关
DB_CONNECTION_HOST = DBL.DBL_CONNECTION_HOST
DB_CONNECTION_USER = DBL.DBL_CONNECTION_USER
DB_CONNECTION_PASSWORLD = DBL.DBL_CONNECTION_PASSWORLD
DB_CONNECTION_DATABASE_NAME = DBL.DBL_CONNECTION_DATABASE_NAME

PATH_SEARCHCACHE = "/pyprojects/teacherRating/"
#HTML拼接相关
COMMENTS_HEAD = """<div class="row-content" style="text-align:central" id="commentslist">
      <div class="alert alert-dismissible alert-info">
          <p class="list-group-item-text">"""

COMMENTS_TAIL = """</p>
        </div>
  </div>"""

AUTOFILL_HEAD = "<option value=\""

AUTOFILL_TAIL = "\">"

def getTeacherInfo(name="",id=-1):
    if( name=="" and id==-1 ):
        return "ERROR"
    RESULT = ""
    if(name != ""):
        RESULT = TI.getTeacherInfo(name)
    elif( id != -1):
        RESULT = TI.getTeacherInfobyID(id)
    else:
        return "ERROR"
    if(len(RESULT) == 0):
        return "ERROR"
    print("WebVersion.RequestTeacherInfo->SUCCESS--|\t\tdata=",RESULT)
    return RESULT[0]

def autoFill(word):
    INS = "select  NAME from `tr_teacherlist`    where NAME like('%" + word +"%')"
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    results = cur.fetchall()
    conn.close()
    DS = ""
    i = 0
    for item in results:
        DS = DS + AUTOFILL_HEAD + str(item[0]) + AUTOFILL_TAIL
        i+=1
        if(i>8):
            break
    if(len(DS) < 16):
        return ""
    return DS

def refreshLikes(id):
    LIKES_HEAD = """<a class="btn btn-raised btn-success" href="javascript:onLike();">赞("""
    LIKES_TAIL = """)<div class="ripple-container"></div></a>
                                <a class="btn btn-raised btn-danger" href="javascript:onDislike();">不赞("""
    TAIL = """)<div class="ripple-container"></div></a> &nbsp;&nbsp;&nbsp;&nbsp;
                                <br/>                               <br/>
                                <a href="javascript:onFillinfo();" class="btn btn-link">补全/修改缺失信息</a>
                                <div class="list-group-separator"></div>"""
    TEACHER = TI.getTeacherInfobyID(str(id))
    LIKES = str(TEACHER[0][3])
    DISLIKES = str(TEACHER[0][4])
    RSD = LIKES_HEAD + LIKES + LIKES_TAIL + DISLIKES + TAIL
    return RSD

def autoRegiste():
    UID = gennerateUID()
    while(TI.registeUser(UID) == "ERROR"):
        UID = gennerateUID()
    print("--->New User Registe:",UID)
    return UID

def addOneUpWeb(atype,id,UID):
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    #判断该用户之前是否已经存在选中
    INS = "SELECT TEACHERLIST FROM  `tr_userlist` WHERE UID=" + "\"" + UID + "\""
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit()
    teacherList = cur.fetchall()
    teacherList = str(teacherList[0])
    teacherList = teacherList.replace("(","")
    teacherList = teacherList.replace(")","")
    teacherList = teacherList.replace("'","")
    teacherList = teacherList[0:len(teacherList)-1]
    print(teacherList)
    if(teacherList.find("NULL") > -1):
        teacherList = ""
        INS = "UPDATE  `tr_userlist` SET TEACHERLIST=\"\" WHERE UID=" + "\"" + UID + "\""
        print("Excute:",INS)
        cur.execute(INS)
        conn.commit()
    #ldlist: teacherid:ldtype-sum,
    ldlist = readLDlist(teacherList)
    teacherJudge = "NO"
    tpos = 0
    FOUND = False
    for td in ldlist:
        if str(td[0]) == str(id):
            if str(td[1]) == "L" and atype == "LIKE":
                if int(td[2]) >= 10:
                    print("UID=",UID,"对","ID=",id,"的老师已经累计点【赞】10次！已禁止继续操作！")
                    return "你已经对这个老师累计点了10次赞了！这个老师已经不能再点了，要不换个老师继续？或者，你写写评论？"
                teacherJudge = "LIKE"
                FOUND = True
                break
            else:
                if str(td[1]) == "D" and atype == "DISLIKE":
                    if int(td[2]) >= 10:
                        print("UID=",UID,"对","ID=",id,"的老师已经累计点【不赞】10次！已禁止继续操作！")
                        return "ERROR:错误！你已经对这个老师累计点了10次不赞了！这个老师已经不能再点了，要不换个老师继续？或者，你写写评论？"
                    teacherJudge = "DISLIKE"
                    FOUND = True
                    break
        tpos+=1
    if(FOUND == False):
        if teacherJudge == "NO":
            teacherJudge = atype
        ldlist.append([str(id),teacherJudge[0],"0"])
        tpos = len(ldlist) - 1
    #进行正常更新
    INS = "UPDATE  `tr_teacherlist` SET "
    if atype == "LIKE":
        INS = INS + "LIKES = LIKES +1 WHERE ID =" + str(id)
        ldlist[tpos][2] = str(int(ldlist[tpos][2]) + 1)
    elif atype == "DISLIKE":
        INS = INS + "DISLIKES = DISLIKES +1 WHERE ID =" + str(id)
        ldlist[tpos][2] = str(int(ldlist[tpos][2]) + 1)
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit() 
    INS = "UPDATE `tr_userlist` SET TEACHERLIST= " +  makeLDlist(ldlist) + "WHERE UID=" + "\"" + UID + "\""
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit() 
    conn.close()
    return "OK"


def getRankList(ltype):
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    #判断请求列表类型
    POSITIVENAME = ""
    NAGAVITIVENAME = ""
    INS = ""
    INSN = ""
    bl = False
    if ltype == "ld": 
        INS = "SELECT * FROM `tr_teacherlist` ORDER BY  `LIKES`  DESC LIMIT 10"
        INSN = "SELECT * FROM `tr_teacherlist` ORDER BY  `DISLIKES`  DESC LIMIT 10"
        POSITIVENAME = "最【赞】老师排行榜"
        NAGAVITIVENAME = "最【不赞】老师排行榜"
    elif ltype == "score":
        INS = "SELECT * FROM  `tr_teacherlist` ORDER BY  `RATING` DESC ,  `LIKES` DESC LIMIT 10"
        INSN = "SELECT * FROM `tr_teacherlist` WHERE RATING!=0"
        POSITIVENAME = "好评率最高老师排行榜"
        NAGAVITIVENAME = "好评率最低排行榜"
        bl = True
    #正表
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit()
    teacherList = cur.fetchall()
    ranklist = ""
    rk = 1
    ranklist = HS.STRING_HEAD_TITLE_RANKLIST + POSITIVENAME + HS.STRING_MID_TITLE_RANKLIST
    for teahcer in teacherList:
        #	ID  NAME  RATING  LIKES   DISLIKES  SUBJECT  SCHOOL  GENDER
        #    0   1      2      3         4        5         6       7
        tl = ""
        tl = "<tr><td>" + str(rk) + "</td><td>" + str(teahcer[1]) + "</td><td>" + str(teahcer[6]) + "->" + str(teahcer[5])   + "</td><td><strong>" + str(teahcer[3]) + "</strong> / " + str(teahcer[4]) + " --> " + str(teahcer[2]) +"</td></tr>" 
        if bl == True:
            tl = "<tr><td>" + str(rk) + "</td><td>" + str(teahcer[1]) + "</td><td>" + str(teahcer[6]) + "->" + str(teahcer[5])  + "</td><td>" + str(teahcer[3]) + " / " + str(teahcer[4]) + " --> <strong>" + str(teahcer[2]) +"</strong></td></tr>"      
        ranklist += tl
        rk+=1
    ranklist = ranklist + HS.STRING_TAIL_RANKLIST
    #负表
    print("Excute:",INSN)
    cur.execute(INSN)
    conn.commit()
    teacherList = cur.fetchall()
    pp = []
    if bl == True:
        teacherList = sorted(teacherList ,key=lambda x:x[2])
        x = 0
        for teacher in teacherList:
            if x > 10:
                break
            pp.append(teacher)
            x+=1
        teacherList = pp
    rk = 1
    ranklist = ranklist + HS.STRING_HEAD_TITLE_RANKLIST + NAGAVITIVENAME + HS.STRING_MID_TITLE_RANKLIST
    for teahcer in teacherList:
        #	ID  NAME  RATING  LIKES   DISLIKES  SUBJECT  SCHOOL  GENDER
        #    0   1      2      3         4        5         6       7
        tl = ""
        tl = "<tr><td>" + str(rk) + "</td><td>" + str(teahcer[1]) + "</td><td>" + str(teahcer[6]) + "->" + str(teahcer[5])  + "</td><td>" + str(teahcer[3]) + " / <strong>" + str(teahcer[4]) + "</strong> --> " + str(teahcer[2]) +"</td></tr>" 
        if bl == True:
            tl = "<tr><td>" + str(rk) + "</td><td>" + str(teahcer[1]) + "</td><td>" + str(teahcer[6]) + "->" + str(teahcer[5])  + "</td><td>" + str(teahcer[3]) + " / " + str(teahcer[4]) + " --> <strong>" + str(teahcer[2]) +"</strong></td></tr>"      
        ranklist += tl
        rk +=1
    ranklist = ranklist + HS.STRING_TAIL_RANKLIST

    return ranklist

def getSearchTags():
    #整合文件
    sl = []
    f = open(PATH_SEARCHCACHE+"searchcache",'r')
    for x in f:
        x = x.replace("\n","")
        x = x.replace("\r","")
        if x == "" or x == " ":
            continue
        xx = 0
        FOUND = False
        for xxx in sl:
            if xxx[0].find(x) > -1:
                sl[xx][1]+=1
                FOUND = True
                break
            xx+=1
        if FOUND == False:
            sl.append([x,1])
    f.close()
    sl  = sorted(sl,key=lambda x:x[1],reverse=True)
    #生成标签
    TAG_HEAD = "<a href=\"" 
    TAG_MID = "\" target=\"_blank\" class=\"btn btn-raised btn-link\">"
    TAG_TAIL = "</a>"
    x = 1
    DD = "<p class=\"text-success\"><strong>大家最近在搜：</strong></p>"
    for tt in sl:
        DD = DD + TAG_HEAD + "trs\\teacher\\" + tt[0] + TAG_MID + tt[0] +"(" + str(tt[1]) + ")" + TAG_TAIL + "&nbsp;&nbsp;"
        if x%5==0:
            DD+="<br/>"
        if x>9:
            break
        x+=1
    return DD

def addMail(mailaddr):
    #检查是否存在
    INS = "SELECT * FROM `tr_subscriber` WHERE EMAIL=\"" + mailaddr +"\""
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    result = cur.fetchall()
    FOUND = False
    if(len(result) != 0):
        conn.close()
        return "ERROR:请不要重复订阅！"
    INS = "INSERT `tr_subscriber` SET EMAIL=\"" + mailaddr +"\""
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    conn.close()
    return "OK"
    

#help function 
def gennerateUID():
    #生成30个随机数
    CHARSET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    i=0 
    uid = ""
    cpos = ""
    while i<24:
        mpt = str(random.randint(0, 9))
        cpos += CHARSET[random.randint(0,25)]
        if mpt == '3' or mpt == '5' or mpt == '7' or mpt == '8':
            uid += mpt + cpos
            cpos = ""
        else:
            uid += mpt + cpos
            cpos = ""
        i+=1
    return uid

def readLDlist(raw):
    # N:V-NUM,N:V-NUM,N:V-NUM,N:V-NUM,
    if len(raw) < 2:
        return []
    LDB = raw.split(",")
    DATA = []
    for x in LDB:
        if len(x) >2:
            NT = x.split(":")
            RT = NT[1].split("-")
            DATA.append( [ NT[0],RT[0],RT[1] ] )
            #             NAME  VTYPE  NUMSUM
    return DATA

def makeLDlist(DATA):
    # N:V-NUM,N:V-NUM,N:V-NUM,N:V-NUM,
    LD = ""
    for x in DATA:
        LD = LD + x[0]  + ":" + x[1] + "-" + x[2] + ","
    LD =  "\"" + LD + "\""
    return LD



    
    