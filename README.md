#成信好老师#

这里是 [成信好老师http://trs.akakanch.com](http://trs.akakanch.com)项目的源代码。包括了前端和后端。前端主要以JavaScript为主。后端主要以Python为主。Python版本为Python3.5

如果你对该份代码有任何问题，请联系：[kanch@akakanch.com](kanch@akakanch.com)

理论上讲，成信好老师这个站点会运行到我毕业（2019年）

######关于Android客户端【弃用】
原来是想的以客户端形式分发，后来根据@misszhang的建议，做成了Web版本，当时客户端 已经基本完成了。不过现在看来Android客户端已经作废，故同样上传到GitHub上来。

Android项目需要Android Studio 2.3及以上打开。

---
##文件结构说明

###**【Web】**
/Web/
####文件夹：
    worklib：这里存放了用来执行交互的python脚本
    templates：这里存放了网页以及模版
    statics：这里主要存放网页的css文件以及js文件
###文件：
    index.py：这是python flask框架的主程序脚本
    /worklib/database.py：这里存放了数据库的相关信息
    /worklib/htmlstring.py：这里存放了用于组合HTML代码的字符段

###**【Utilities】**
/Utilities/

这里是一些常用工具集合（部署在GAE上的）
####文件夹：
    null
###文件：
    null

###**【Android】**
/Android/

以下文件路径：\TeacherRating\app\src\main\java\com\kanchsproject\teacherrating
###文件：
    Comments.java:从服务器获取评论并显示
    FillLostInfo.java:补全/修改老师信息
    HttpUtils.hava:用于和服务器进行POST/GET交互
    MainActivity.java:程序主activity
    Teacherinfo.java:从服务器获取老师信息并显示，处理点赞/不赞
    WebClient.java:用于以HTTP GET的方式打开一个URL并获取信息
    WriteComments.java:写评论


---
##数据库：
数据库(kappdb_teacher_rating)主要包括4个表：

    tr_teacherlist：存放老师的基本信息
    tr_teacher_comments：存放老师的评论信息
    tr_userlist：存放UID以及其点赞/不赞列表
    tr_subscriber：存放网站订阅者的邮件地址
######每个表的结构：

tr_teacherlist：

	
    ID NAME RATING LIKES DISLIKES SUBJECT SCHOOL GENDER

tr_teacher_comments：

	
    ID NAME SUM FILENAME

tr_userlist：

    UID TEACHERLIST COMMENTS

tr_subscriber：

    EMAIL

