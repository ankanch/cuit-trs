#coding=utf-8
import os
import threading
import datetime
import time

#执行间隔（秒）
CHECK_PER_SECONDS = 29*60   

##################################
#该脚本用来定时运行scripts目录下的python脚本
#v1.0
##################################

def runScripts():
    #for script in os.listdir("scripts"): Windows
    for script in os.listdir("./scripts"):
        print(script)
        if os.path.isfile(os.path.join("./scripts",script)) == True:
            #在这里执行脚本
            cmd = "sudo python3 ./scripts/" + script
            print("\tExceute->",cmd)
            os.system(cmd)



#################################################################################
#                                   脚本逻辑
#################################################################################
timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
print("\nPythonScript Auto Excutor now running...")
print(os.listdir("./scripts"))
print("Application will exceute script in scripts folder every ",CHECK_PER_SECONDS/60," minutes.\n\n")
print(timestr,">>>starting initial scripts execution...")
runScripts()
timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
print(timestr,">>>initial execution finished!")
while True:
    time.sleep(CHECK_PER_SECONDS)
    timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    print(timestr,">>>starting  execution...")
    runScripts()
    timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    print(timestr,">>>execution finished!")