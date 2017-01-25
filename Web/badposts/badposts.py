import datasourceconfig.database_settings as DBS
import pymysql as SQL
import datetime
import worklib.htmlstring as STR


#将从数据库加载的曝光数据根据支持人数组合成表格
def makeUpTable(tupdata):
    TABLESTR = ""
    #我们将支持人数超过50的标记为热门（暂时）
    #badpost = [ID,TITLE,CONTENT,DATE,UP]
    #内容最多6排（333字）
    pdata = reversed(tupdata)
    for badposts in pdata:
        pstr = ""
        if badposts[4] >=50:
            pstr = STR.BP_HEAD_HOT
        else:
            pstr = STR.BP_HEAD_NORMAL
        content = badposts[2]
        if len(content) > 333:
            content = badposts[2][0:333]+"......"
        #content = content.replace("<","--")
        content = content.replace("\n","<br/>")
        pstr +=  badposts[1] + STR.BP_A_CONTENT + content + STR.BP_B_DATE \
                + badposts[3].strftime('%Y-%m-%d %H:%M:%S') \
                + STR.BP_C_UPS + str(badposts[4]) + STR.BP_D_LINK + str(badposts[0]) + STR.BP_TAIL
        TABLESTR += pstr
    if TABLESTR == "":
        TABLESTR = "NULL"
    return TABLESTR

#从数据库加载指定条数的曝光数据，按照时间排序
def queryBadposts(qsum,curid):
    SEL = ""
    if int(curid) == 0:
        SEL = "SELECT * FROM `badposts` WHERE ID<=(SELECT MAX(ID) FROM `badposts`) ORDER BY ID DESC LIMIT 5"
    else:
        SEL = "SELECT * FROM `badposts` WHERE (ID<" + curid + " AND ID>=" + str(int(curid) - int(qsum)) + ")"
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    #找出最小ID值，方便继续加载
    minid = 999999999999
    for bp in result:
        if bp[0] <= minid:
            minid = bp[0]
    #minid = min(result,lambda x : x[0])
    #第一次加载需要反转
    if int(curid) == 0:
        pdata = tuple(reversed(result))
        return pdata,str(minid)
    return result,str(minid)


#插入新的曝光数据到数据库
def insertBadposts(title,content):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "INSERT INTO `badposts`(`TITLE`, `CONTENT`, `DATE`, `UP`) VALUES (\""
    INS = INS + title +"\",\"" + content + "\",\"" + str(datetime.datetime.now()) + "\",1)"
    DBCUR.execute(INS)
    DBCONN.commit()
    SEL = "SELECT `ID` FROM `badposts` WHERE TITLE=\"" + title +"\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result[0][0]

#获取指定曝光的信息
def getBadposts(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    INS = "SELECT * FROM `badposts` WHERE ID=" + str(xid)
    DBCUR.execute(INS)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result[0]


#搜索包含指定关键字的曝光数据
def searchFor(tags):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `badposts` WHERE TITLE LIKE'%" + tags + "%' UNION SELECT * FROM `badposts` WHERE CONTENT LIKE'%"  + tags + "%' "
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    return result

#支持了某一篇曝光
def support(xid):
    DBCONN = SQL.connect(host=DBS.HOST_CH, port=3306,user=DBS.USER_CH,passwd=DBS.PASSWORD_CH,db=DBS.NAME_CH,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `badposts` WHERE  ID= " + str(xid)
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    if len(result) == 0:
        return False   #false为未查找到指定回帖
    ADD = "UPDATE `badposts` SET `UP`=`UP`+1 WHERE `ID`=" + str(xid)
    DBCUR.execute(ADD)
    DBCONN.commit()
    DBCUR.close()
    DBCONN.close()
    return True


###########################3
#数据库辅助函数
###########################

