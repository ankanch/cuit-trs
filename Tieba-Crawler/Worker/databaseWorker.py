import pymysql as SQL
import Config.config as CFG 

#
#该模块是用来将数据提交到数据库
#由于pymysql的问题，只能单线程。
#提交逻辑：每2500条数据进行一次提交
#
#
