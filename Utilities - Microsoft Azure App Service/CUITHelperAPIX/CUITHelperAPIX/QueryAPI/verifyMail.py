from CUITHelperAPIX.QueryAPI import database as DBS
import pymysql as SQL

def checkHash(hashdata):
    DBCONN = SQL.connect(host=DBS.HOST, port=3306,user=DBS.USER,passwd=DBS.PASSWORD,db=DBS.NAME,charset='UTF8')
    DBCONN.set_charset('utf8mb4')
    DBCUR = DBCONN.cursor()
    DBCUR.execute("SET names 'utf8mb4'")
    
    DBCUR.close()
    DBCONN.close()
    return True
