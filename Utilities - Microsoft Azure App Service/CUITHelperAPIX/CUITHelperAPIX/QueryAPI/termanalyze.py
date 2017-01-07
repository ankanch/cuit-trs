import CUITHelperAPIX.QueryAPI.database as DBS
import pymysql as SQL
import datetime


def searchForInclude(word):
    DBCONN = SQL.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT `AUTHOR`,`DATE`  FROM `postdata` WHERE `CONTENT`  Like \"%" + word + "%\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result



def statisANDTimeline(datasource):
    usercount = []  #[ [name],[wordcount],[sumcount] ]
    timeline = []   #[[time],[count]]
    for data in datasource:
        author = data[0]
        date = data[1]
        AF = False
        iaf = 0
        DF = False
        idf = 0

        for a in usercount:
            if a[0] == author:
                AF = True
                break
            iaf+=1
        if AF == False:
            usercount.append([author,1,"N/A"])
        else:
            usercount[iaf][1]+=1

        for d in timeline:
            if d[0] == date:
                DF = True
                break
            idf +=1
        if DF == False:
            timeline.append([date,1])
        else:
            timeline[idf][1]+=1
    return usercount,timeline

def slice(usercount,timeline):
    #gather time line
    tl = []
    vl = []
    timeline = sorted(timeline, key=lambda data: data[0])
    for time in timeline:
        pstr = str(time[0].year) +'-' +str(time[0].month) +'-' +str(time[0].day)
        tl.append(pstr)
        vl.append(time[1])
    timevl = str(tl) + "," + str(vl)
    #sort and gather userlist
    userstr = ""
    usercount = sorted(usercount, key=lambda user: user[1],reverse=True)
    i = 0
    for user in usercount:
        pstr = user[0] + ":" + str(user[1]) + ":" + str(user[2])
        userstr += pstr + ","
        if i == 10:
            break
        i+=1
    return timevl,userstr

def saveToDB(userstr , timevl,term):
    DBCONN = SQL.connect(host=DBS.HOST_TD, port=3306,user=DBS.USER_TD,passwd=DBS.PASSWORD_TD,db=DBS.NAME_TD,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "INSERT INTO `term_data`( `TERM`, `MOSTUSER`, `TIMELINE`, `COUNT`) VALUES (" +"\""+ term+"\",\""+ userstr+"\",\"" +timevl+"\","+"1" +")"
    DBCUR.execute(INS)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()


def checkExist(term):
    DBCONN = SQL.connect(host=DBS.HOST_TD, port=3306,user=DBS.USER_TD,passwd=DBS.PASSWORD_TD,db=DBS.NAME_TD,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "SELECT * FROM `term_data` WHERE TERM=\"" + term +"\""
    DBCUR.execute(INS)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return False
    else:
        return True

