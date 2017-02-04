import pymysql as SQL
import Config.config as CFG 
import Config.database as DB

#
#该模块是用来将数据提交到数据库
#由于pymysql的问题，只能单线程。
#提交逻辑：每2500条数据进行一次提交
#
#

#初始化数据库
print(">>>initialzing database connections...",end="")
DBCONN = SQL.connect(host=DB.HOST, port=3306,user=DB.USER,passwd=DB.PASSWORD,db=DB.NAME,charset='UTF8')
DBCONN.set_charset('utf8mb4')
DBCUR = DBCONN.cursor()
DBCUR.execute("SET names 'utf8mb4'")
print("\r>>>database connected.")

#提交worker，给出指定需要提交的列表，worker会进行提交事物
#下面这个函数提交事务均通过DBCUR来实现
def databaseWorker(datalist,type_="INSERT"):
    INSSUFFIX = "INSERT INTO `postdata2`(`POSTID`, `TIEBANAME`, `AUTHOR`, `CONTENT`, `DATE`, `REPLYTO`, `LINK`) VALUES ("
    for item in datalist:
        #结构： [ [帖子ID,当前页码,[replydata]],[帖子ID,当前页码,[replydata]],..... ]
        # replydata = [发帖用户,回帖信息,发帖时间,REPLY_TO]
        #提交的时候需要去除一些非法字符比如双引号无效字符比如逗号
        replycontent = item[2][1].replace("\"","'")
        replycontent = replycontent.replace(" ","")
        replycontent = replycontent.replace("_","-")
        replycontent = replycontent.replace("%","/")
        replycontent = replycontent.replace("\\","")
        INS = INSSUFFIX + "\"" + item[0] + "\",\"" + CFG.TIEBA_NAME + "\",\"" + item[2][0] \
                + "\",\"" + replycontent.replace("[","【") + "\",\"" + item[2][2] + "\",\"" + item[2][3] + "\",\"" + item[1] + "\")"
        try:
            DBCUR.execute(INS)
        except Exception as e:
            ff = open("aaa.txt","wb")
            ff.write(INS.encode("utf-8","ignore"))
            ff.close()
            exit()
    DBCONN.commit()
    return True