import pymysql as SQL
import database as DBS
import os
import ast
import graphicsData as GRAPH

DB_NAME = DBS.NAME
DB_HOST = DBS.HOST
DB_USER = DBS.USER
DB_PASSWORD = DBS.PASSWORD
PATH_SUFFIX = "Cache/ATZresult/"

#该脚本用于根据用户活跃时间段对用户进行分类
#application start
os.system("cls")
print("cuit tieba user analyzier\nthis script is used to classify user by active timezone.\napplication start.\nconnecting to the database...")
#==
conn = SQL.connect(host=DB_HOST, port=3306,user=DB_USER,passwd=DB_PASSWORD,db=DB_NAME,charset='UTF8')
conn.set_charset('utf8mb4')
cur = conn.cursor()
print("downloading user active timezon...")
SEL = "SELECT `USER`,TIMEZONE FROM `useranalyze` WHERE 1"
cur.execute(SEL)
conn.commit()
cur.close()
conn.close()
result = cur.fetchall()
ff = open(PATH_SUFFIX+"result.txt","w")
ff.write(str(result))
ff.close()
print(len(result)," pieces of data retrived.\n+Start classify.")
#============开始分类==========
#【分类思路】
#首先要排除无效数据，即发帖量小于 10 的 
#然后，将 User-ActiveTimeZone-Martix 转化为 User-ActivePeak-Martix
#=============================
print("---Start convert User-ActiveTimeZone Martix (UAT) to User-ActivePeak Martix (UAP).")
i=0
skipped_null = 0
skipped_invaild = 0
sumx = len(result)
presult = [] # [ [用户名,[peak,peak-index]],[一条数据],... ]
for user in result:
    i+=1
    print("-----processing... ",i,"/",sumx,end="")
    # add process code here
    # user.0 for username user.1 for active timezone
    if user[1] != "NULL":
        uat = ast.literal_eval(user[1])
        if sum(uat) > 0:  #在这里控制忽略用户条件
            #下面为结果集结构， [ [用户名,[peak,peak-index]],[一条数据],... ]
            presult.append([user[0],[max(uat),[x for x in range(len(uat)) if uat[x] == max(uat)][0]]])
        else:
            skipped_invaild+=1
    else:
        skipped_null+=1
    print("",end="\r")
print("-----UAT to UAP done.")
print("---UAT to UAP finished with",skipped_invaild,"invaild users skipped,",skipped_null,"NULL data skipped.")
#print(str(presult))
print("---Compute Tieba ActiveTimeZone...")
tiebaActiveTimeZone = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for item in  presult:
    tiebaActiveTimeZone[item[1][1]] += item[1][0]
#print(str(tiebaActiveTimeZone))  # show result martix
kp = input("---Show Tieba Active TimeZone Graph?(Y/N)")
if kp == "Y" or kp == "y": 
    xValueList = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
    GRAPH.linePlotGraphics("时间","发帖量",xValueList,tiebaActiveTimeZone,graphicTitle='成都信息工程大学贴吧活跃时间段分析（基于'+str(len(result))+"名用户)")

print("+Application finised.")