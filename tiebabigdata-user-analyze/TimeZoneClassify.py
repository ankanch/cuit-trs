import pymysql as SQL
import database as DBS
import os
import ast
import random
import math
import graphics as GRAPH
from matplotlib import pyplot as plt
import numpy as np

DB_NAME = DBS.NAME
DB_HOST = DBS.HOST
DB_USER = DBS.USER
DB_PASSWORD = DBS.PASSWORD
PATH_SUFFIX = "Cache/ATZresult/"
PATH_DATA = "Data/"
EXTREME = 400
CONVERGENCE = 0.001  # 当前质心与上一质心的收敛范围
CONVERGENCE_CosSim = 1.00000000000001  # 当前质心与上一质心的收敛范围(余弦相似性版本)(需要越来越接近1)
INGORE_POST_UNDER = 10   #要忽略发帖量小于指定值的用户

#计算两点间距离
def calDistance(p1,p2):
    #[用户名,[24维度]]
    total_asum = 0.0
    for d1,d2 in zip(p1[1],p2[1]):
        total_asum += (d1 - d2)**2
    dist = math.sqrt(total_asum)
    return dist

#计算两点间距离-余弦相似性
#返回cosx的倒数
def calDistanceCosSim(p1,p2):
    #[用户名,[24维度]]
    total_asum = 0.0
    neo = 0.0
    deo_1 = 0.0
    deo_2 = 0.0
    for d1,d2 in zip(p1[1],p2[1]):
        neo += d1*d2
        deo_1 += d1*d1
        deo_2 += d2*d2
    cosx = neo/(math.sqrt(deo_1)*math.sqrt(deo_2))
    #为了不改变下面的主算法，我们这里返回cosx的倒数
    if cosx != 0:
        cosx = 1/cosx
    else:
        return 1
    return cosx

#检查是否收敛,参数分别为上一次的质心列表和当前质心列表
def checkConvergence(lcl,ccl):
    for c in zip(lcl,ccl):
        #[用户名,[peak,peak-index]]
        if calDistance(c[0],c[1]) > CONVERGENCE:
            return False
    return True

#检查是否收敛,参数分别为上一次的质心列表和当前质心列表(余弦相似性版本)
#(需要越来越接近1)，因为calDistanceCosSim返回的倒数
def checkConvergenceCosSim(lcl,ccl):
    for c in zip(lcl,ccl):
        #[用户名,[24维度时间数据]]
        dsv = calDistanceCosSim(c[0],c[1])
        #print("dsv=",dsv,"CONVERGENCE_CosSim",CONVERGENCE_CosSim)
        if dsv > CONVERGENCE_CosSim:
            #未收敛
            return False
    return True

#根据一个点集求出平均点(求出新质心)
def calNewCenter(pl):
    sumv = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    lenl = len(pl)
    #相加
    #[用户名,[24维]]
    for user in pl:
        i=0
        for v in user[1]:
            sumv[i]+=v
            i+=1
    #平均
    avgv = []
    for v in sumv:
        avgv.append(v/lenl)
    return ["X@X",avgv]


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
print("---Start convert User-ActiveTimeZone Martix (UAT) ")
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
            #下面为结果集结构， [ [用户名,[ActiveTimeZone-Martix（24维）]],[一条数据],... ]
            presult.append([user[0],uat])
        else:
            skipped_invaild+=1
    else:
        skipped_null+=1
    print("",end="\r")
print("---UAT literal_eval finished with",skipped_invaild,"invaild users skipped,",skipped_null,"NULL data skipped.")
#print(str(presult))
print("---Compute Tieba ActiveTimeZone...")
tiebaActiveTimeZone = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for item in  presult:
    tiebaActiveTimeZone = [x+y for x,y in zip(tiebaActiveTimeZone, item[1])]
#print(str(tiebaActiveTimeZone))  # show result martix
kp = input("---Show Tieba Active TimeZone Graph?(Y/N)")
if kp == "Y" or kp == "y": 
    print('-----loading graph...')
    xValueList = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
    GRAPH.linePlotGraphics("时间","发帖量",xValueList,tiebaActiveTimeZone,graphicTitle='成都信息工程大学贴吧活跃时间段分析（基于'+str(len(result))+"名用户)")
#接下来是根据用户最多发帖时间来进行分类
#将 presult 映射到 ActiveTimeZone-Martix 坐标系上，然后进行聚类
#根据上面的图像来聚类（目前数据主要分成3类）
# x轴：24小时时间值，y轴：发帖量  每个点隐含：用户名
# 这里采用 K-Means算法 这里k=3
# 处理元数据： [ [用户名,[ActiveTimeZone-Martix（24维）]],[一条数据],... ]
#首先去除异常值
print("---delete extreme value.")
i=0
for user in presult:
    for v in user[1]:
        if int(v) > EXTREME:
            print("del ",str(presult[i]))
            del presult[i]
            break
    i+=1 
#是否显示聚类前的样本空间
kp = input('---would you like to see the sample space graph?(Y/N)')
if kp == "Y" or kp == "y":
    print("-----loading graph...")
    x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for user in presult:
        with plt.style.context('fivethirtyeight'):
            plt.plot(x, user[1])
    plt.title(str(len(presult)))
    plt.show()
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
        #欧几里德距离
        #da = calDistance(user,cca)
        #db = calDistance(user,ccb)
        #dc = calDistance(user,ccc)
        #余弦相似性
        da = calDistanceCosSim(user,cca)
        db = calDistanceCosSim(user,ccb)
        dc = calDistanceCosSim(user,ccc)
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
        if checkConvergenceCosSim([cca,ccb,ccc],[lca,lcb,lcc]) == True:
        #if checkConvergence([cca,ccb,ccc],[lca,lcb,lcc]) == True:
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
print("calculate average active timezone of those three clusters.")
c1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
c2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
c3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
for v in lal:
    c1 = [x+y for x,y in zip(c1, v[1])]
    with plt.style.context('fivethirtyeight'):
        plt.plot(x, v[1])
print("total=",c1)
c1 = [int(x/len(c1)) for x in c1]
print("avg=",c1)
plt.show()
for v in lbl:
    c2 = [x+y for x,y in zip(c2, v[1])]
    with plt.style.context('fivethirtyeight'):
        plt.plot(x, v[1])
print("total=",c2)
c2 = [int(x/len(c2)) for x in c2]
print("avg=",c2)
plt.show()
for v in lcl:
    c3 = [x+y for x,y in zip(c3, v[1])]
    with plt.style.context('fivethirtyeight'):
        plt.plot(x, v[1])
print("total=",c3)
c3 = [int(x/len(c3)) for x in c3]
print("avg=",c3)
plt.show()
print("loading graph.")
colors = ['g','r','y','k']
with plt.style.context('fivethirtyeight'):
    plt.plot(x, c1)
    plt.plot(x, c2)
    plt.plot(x, c3)
plt.show()
print("+Application finised.")