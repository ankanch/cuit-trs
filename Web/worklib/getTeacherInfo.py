import pymysql
import linecache
import worklib.database as DBL

PATH_COMMENTS = "/pyprojects/teacherRating/comments/"

SYMBOL_CLRF = "CSYZL"
SYMBOL_SUFFIX_COMMENTS = ".comments"

#数据库相关
DB_CONNECTION_HOST = DBL.DBL_CONNECTION_HOST
DB_CONNECTION_USER = DBL.DBL_CONNECTION_USER
DB_CONNECTION_PASSWORLD = DBL.DBL_CONNECTION_PASSWORLD
DB_CONNECTION_DATABASE_NAME = DBL.DBL_CONNECTION_DATABASE_NAME

#URL functions
def registeUser(UID):
    print("checking user exist...")
    if(checkUser(UID) == False):
        return "ERROR"
    INS = "INSERT INTO `tr_userlist`(`UID`, `TEACHERLIST`, `COMMENTS`) VALUES (\"" + UID  +"\",\"NULL\",\"NULL\")"
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    return "OK"



def getTeacherInfo(name):
    INS = "SELECT * FROM `tr_teacherlist` where NAME=\"" + name +"\""
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    results = cur.fetchall()
    conn.close()
    return results

def getRatingList(UID):
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    INS = "SELECT TEACHERLIST FROM  `tr_userlist` WHERE UID=" + UID
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit()
    teacherList = cur.fetchall()
    ratingLIst = teacherList[0]
    return ratingLIst

def getTeacherInfobyID(id):
    INS = "SELECT * FROM `tr_teacherlist` where ID= "+id
    #INS = "SELECT * FROM `tr_teacherlist` where LIKES=0"
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    results = cur.fetchall()
    conn.close()
    return results

def addOneUp(atype,id,UID):
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    #判断该用户之前是否已经存在选中
    INS = "SELECT TEACHERLIST FROM  `tr_userlist` WHERE UID=" + UID
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit()
    teacherList = cur.fetchall()
    teacherList = str(teacherList[0])
    teacherList = teacherList.replace("(","")
    teacherList = teacherList.replace(")","")
    teacherList = teacherList.replace("'","")
    teacherList = teacherList[0:len(teacherList)-1]
    #print(teacherList)
    if(teacherList.find("NULL") > -1):
        teacherList = ""
        INS = "UPDATE  `tr_userlist` SET TEACHERLIST=\"\" WHERE UID=" + UID
        #print("Excute:",INS)
        cur.execute(INS)
        conn.commit()
    SID_POS = teacherList.find(str(id))
    NOW = "X"
    UINS = "1234"
    if( SID_POS >= 0 and UID!="123"):
        # N:V,N:V,N:V,N:V,
        teacherJudge  = teacherList[SID_POS+len(str(id))+1:teacherList.find(",",SID_POS)]
        if teacherJudge == "L":
            UINS = "UPDATE  `tr_teacherlist` SET  LIKES = LIKES -1 WHERE ID =" + str(id)
            NOW = "L"
        else:
            UINS = "UPDATE  `tr_teacherlist` SET  DISLIKES = DISLIKES -1 WHERE ID =" + str(id)
            NOW = "D"
        print("Excute:",UINS)
        cur.execute(UINS)
        conn.commit()
        prefix = teacherList[0:SID_POS]
        suffix = teacherList[teacherList.find(",",SID_POS)+1:len(teacherList)]
        teacherList = prefix + suffix
    #进行正常更新
    INS = "UPDATE  `tr_teacherlist` SET "
    TYPE  = "x"
    if atype == "LIKE":
        INS = INS + "LIKES = LIKES +1 WHERE ID =" + str(id)
        TYPE = "L"
    elif atype == "DISLIKE":
        INS = INS + "DISLIKES = DISLIKES +1 WHERE ID =" + str(id)
        TYPE = "D"
    if TYPE != NOW:
        print("Excute:",INS)
        cur.execute(INS)
        INS = "UPDATE  `tr_userlist` SET TEACHERLIST=TEACHERLIST+\""+ str(id) +",\"WHERE UID=" + UID
        #print("Excute:",INS)
        cur.execute(INS)
        conn.commit()
        teacherList = teacherList + str(id) + ":" + TYPE + "," 
        INS = "UPDATE  `tr_userlist` SET TEACHERLIST=\""+ teacherList +"\"WHERE UID=" + UID
        #print("Excute:",INS)
        cur.execute(INS)
        conn.commit() 
    else:
        print("Similarity data insert!Abort by application.")
    conn.close()
    return "OK"

    


def addComment(id,comment):
    INS = "UPDATE  `tr_teacher_comments` SET SUM = SUM +1 WHERE ID =" + str(id)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    conn.close()
    comment = comment.replace("\n",SYMBOL_CLRF)
    comment = comment + "\r\n"
    name = findNamebyID(id)
    filename = PATH_COMMENTS + name + SYMBOL_SUFFIX_COMMENTS
    writeComments(filename,comment)
    return "OK"

def getCommentSum(id):
    INS = "SELECT `SUM` FROM `tr_teacher_comments` WHERE ID=" + str(id)
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    results = cur.fetchall()
    conn.close()
    return str(results[0][0])

def getComment(id,linestart,lineend):
    name = findNamebyID(id)
    filename = PATH_COMMENTS + name + SYMBOL_SUFFIX_COMMENTS
    comments = readComments(filename,linestart,lineend)
    comments = str(comments)
    return comments

def fillLostInfo(id,subject="",school="",gender=""):
    print("Recived Teracher Lost Info:",subject,school,gender,id)
    if( subject=="" or school=="" or gender=="" ):
        print(subject,school,gender,id)
        return "ERROR"
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    SUBJECT_SUB = "\"" + subject + "\""
    SCHOOL_SUB = "\"" + school + "\""
    GENDER_SUB = gender
    INS = "UPDATE `tr_teacherlist` SET SUBJECT="+ SUBJECT_SUB +",SCHOOL="+ SCHOOL_SUB +",GENDER="+ GENDER_SUB +" WHERE ID=" + id
    print("Excute:",INS)
    cur.execute(INS)
    conn.commit()
    conn.close()
    return "OK"

#file options AND inner funtion
def writeComments(filename,comments):
    f=open(filename,'a')
    print("Write Comments:",comments)
    f.write(comments)
    f.flush()        
    f.close()

def readComments(filename,linebeg,lineend):
    count = linecount(filename)
    if linebeg > lineend:
        return "ERROR"
    if linebeg > count:
        return "NULL"
    else:
        data = ""
        if lineend <= count:
            x = linebeg
            while x < lineend:
                data = data + linecache.getline(filename,x) + "<br/>"
                x+=1
            return data
        else:
            data = linecache.getlines(filename,linebeg)
            DAT = ""
            for item in data:
                DAT = DAT + item + "<br/>"
            return DAT

def linecount(filename):
    count = -1
    for count, line in enumerate(open(filename)): pass
    return count+1

def findNamebyID(id):
    INS = "SELECT `NAME` FROM `tr_teacherlist` where ID= " + str(id)
    print("Excute:",INS)
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    name = cur.fetchall()
    conn.close()
    name = str(name)
    name = name.replace("(","")
    name = name.replace(")","")
    name = name.replace(",","")
    name = name.replace("'","")
    return name

def checkUser(UID):
    INS = "SELECT UID FROM `tr_userlist` WHERE UID=\"" + UID +"\""
    conn = pymysql.connect(host=DB_CONNECTION_HOST, port=3306,user=DB_CONNECTION_USER,passwd=DB_CONNECTION_PASSWORLD,db=DB_CONNECTION_DATABASE_NAME,charset='UTF8')
    cur = conn.cursor()
    cur.execute(INS)
    conn.commit()
    result = cur.fetchall()
    conn.close()
    if(len(result) != 0):
        return False
    return True