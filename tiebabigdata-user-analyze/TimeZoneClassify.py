import pymysql as SQL
import database as DBS
import os
import ast
import random
import math
import graphics as GRAPH

DB_NAME = DBS.NAME
DB_HOST = DBS.HOST
DB_USER = DBS.USER
DB_PASSWORD = DBS.PASSWORD
PATH_SUFFIX = "Cache/ATZresult/"
PATH_DATA = "Data/"
CONVERGENCE = 0.001  # 当前质心与上一质心的收敛范围
INGORE_POST_UNDER = 10   #要忽略发帖量小于指定值的用户

#计算两点间距离
def calDistance(p1,p2):
    #[用户名,[peak,peak-index]]
     dist = math.sqrt((p1[1][1] - p2[1][1])**2 + (p1[1][0] - p2[1][0])**2)
     return dist

#检查是否收敛,参数分别为上一次的质心列表和当前质心列表
def checkConvergence(lcl,ccl):
    for c in zip(lcl,ccl):
        #[用户名,[peak,peak-index]]
        if calDistance(c[0],c[1]) > CONVERGENCE:
            return False
    return True

#根据一个点集求出平均点(求出新质心)
def calNewCenter(pl):
    sumy=0
    sumx=0
    lenl = len(pl)
    #[用户名,[peak,peak-index]]
    for user in pl:
        sumy += user[1][0]
        sumx += user[1][1]
    return ["X@X",[sumy/lenl,sumx/lenl]]


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
#ff = open(PATH_SUFFIX+"result.txt","w")
#ff.write(str(result))
#ff.close()
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
        if sum(uat) > INGORE_POST_UNDER:  #在这里控制忽略用户条件<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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
    print('-----loading graph...')
    xValueList = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
    GRAPH.linePlotGraphics("时间","发帖量",xValueList,tiebaActiveTimeZone,graphicTitle='成都信息工程大学贴吧活跃时间段分析（基于'+str(len(result))+"名用户)")
#接下来是根据用户最多发帖时间来进行分类
#将 presult 映射到 peak-peak_index 坐标系上，然后进行聚类
#根据上面的图像来聚类（目前数据主要分成3类）
# x轴：24小时时间值，y轴：发帖量  每个点隐含：用户名
# 这里采用 K-Means算法 这里k=3
# 处理元数据： [ [用户名,[peak,peak-index]],[一条数据],... ]
#是否显示聚类前的样本空间
kp = input('---would you like to see the initial peak-peak_index graph?(Y/N)')
if kp == "Y" or kp == "y":
    print("-----loading graph...")
    xval = []
    yval = []
    for user in presult:
        xval.append(user[1][1])
        yval.append(user[1][0])
    GRAPH.Scatterplot("发帖量","时间段",xval,yval,"成都信息工程大学贴吧用户最活跃时间点")
#开始聚类
print("---Start clustering...")
print('-----initial k-means,chooseing 3 random center.')
cca = presult[random.randint(0,len(presult)-1)] # 这3个变量是用来存放当前质心的
ccb = presult[random.randint(0,len(presult)-1)] # 初始状态我们要随机选择3个质心
ccc = presult[random.randint(0,len(presult)-1)] #结构：[用户名,[peak,peak-index]]
lca = []#3个变量用来 
lcb = []#储存上一次质心
lcc = []#所在位置。
lal = [] #这3个列表
lbl = [] #是用来存放对应cluster
lcl = [] #的点的（用户）
FIRST = True
xround = 1
while True:
    print('-----processing #',xround,'round.')
    #print('-----processing #',xround,'round.(center:',str([cca[1],ccb[1],ccc[1]]),")\n")
    del lal[:]
    del lbl[:]
    del lcl[:]
    #聚类
    for user in presult:
        da = calDistance(user,cca)
        db = calDistance(user,ccb)
        dc = calDistance(user,ccc)
        #print(str([da,db,dc]))
        if da <= db:
            if dc <= da:
                lcl.append(user)
            else:
                lal.append(user)
        else:
            if dc <= db:
                lcl.append(user)
            else:
                lbl.append(user)
    #判断是否收敛
    if FIRST == False:
        if checkConvergence([cca,ccb,ccc],[lca,lcb,lcc]) == True:
            break
    #储存上次的质心
    lca = cca
    lcb = ccb
    lcc = ccc
    #计算新质心
    cca = calNewCenter(lal)
    ccb = calNewCenter(lbl)
    ccc = calNewCenter(lcl)
    FIRST = False
    xround +=1
#"""
fa = open(PATH_DATA+"a.txt",'w')
fb = open(PATH_DATA+"b.txt",'w')
fc = open(PATH_DATA+"c.txt",'w')
fa.write(str(lal))
fb.write(str(lbl))
fc.write(str(lcl))
fa.close()
fb.close()
fc.close()
#"""
#绘制聚类后的图像
print("center:",str([cca[1],ccb[1],ccc[1]]))
GRAPH.ScatterplotS("时间","发帖量",[lal,lbl,lcl],[cca[1],ccb[1],ccc[1]],"聚类结果 k=3(收敛："+ str(CONVERGENCE) + "忽略发帖量小于"+str(INGORE_POST_UNDER)+"的用户)")
#GRAPH.Scatterplot("时间","发帖量",[cca[1][1],ccb[1][1],ccc[1][1]],[cca[1][0],ccb[1][0],ccc[1][0]],"聚类结果 k=3")
print("+Application finised.")