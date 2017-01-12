import pymysql as SQL
import datasourceconfig.database_settings as DBS
import ast

#该文件用来处理按单词查询

#该函数用来根据已经查询到的数据生成网页
#返回： ID,时间频率数组，用户使用排名，记录查询次数
def generateByResult(data):
    #	ID编号    TERM词语  MOSTUSER使用量最高的前10用户     TIMELINE时间频率数组  COUNT记录查询次数
    ID= data[0][0]
    TFGdata = []
    ulist = data[0][2]
    timeline = data[0][3]
    count = data[0][4]
    timeline = timeline.replace("],[","@#@")
    timeline = timeline.replace("]","")
    timeline = timeline.replace("[","")
    timeline = timeline.split("@#@")
    gdate  = timeline[0].split(", ")
    value = timeline[1].split(",")
    TFGdata.append(["[" + timeline[0]+"]",value])
    ulist = ulist.split(",")
    userdatatable = generateTableData(ulist)
    return ID,TFGdata,userdatatable,count

#该函数为上一个函数服务，生成表格数据
def generateTableData(userlist):
    TABLE_HEAD = """<tr>
    <td>"""
    TABLE_MID_A = """</td>
    <td>"""
    TABLE_MID_B = """</td>
    <td>"""
    TABLE_MID_C = """</td>
    <td>"""
    TABLE_TAIL = """</td>
    </tr>"""

    RESULTSTR = ""
    i = 0
    for item in userlist:
        if len(item) <=0:
            continue
        pdata = item.split(":")
        RESULTSTR += (TABLE_HEAD + str(i) +TABLE_MID_A +pdata[0] + TABLE_MID_B + pdata[1] + TABLE_MID_C + pdata[2] +TABLE_TAIL)
        i+=1
    return RESULTSTR


#以下为辅助函数


#该函数用来判断待搜索词语是否之前已经被查询过
def checkExistInTD(word):
    DBCONN = SQL.connect(host=DBS.HOST_TD, port=3306,user=DBS.USER_TD,passwd=DBS.PASSWORD_TD,db=DBS.NAME_TD,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    SEL = "SELECT * FROM `term_data` WHERE TERM= \"" + word + "\""
    DBCUR.execute(SEL)
    DBCONN.commit()
    result = DBCUR.fetchall()
    DBCUR.close()
    DBCONN.close()
    if len(result) == 0:
        return False,result
    else:
        return True,result


#该函数用来将时间频率数据按照指定粒度聚合
def ScaleData(timelinedata,scale_factor):
    if scale_factor == 1:
        return timelinedata
    newtldata = [[]]
    datelist = []
    valuelist = []
    ct = 1
    i=0
    stb = 0
    rdl = ast.literal_eval(timelinedata[0][0])
    rvl = ast.literal_eval(str(timelinedata[0][1]))
    for date in rdl:
        if ct != scale_factor:
            stb += int(rvl[i])
            ct+=1
        else:
            datelist.append(date)
            valuelist.append(stb)
            ct = 1
            stb = 0
        i+=1
    newtldata[0].append(datelist)
    newtldata[0].append(valuelist)
    return newtldata