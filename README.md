#成信助手#

这里是 [~~成信好老师~~（现已更名为成信助手）http://trs.akakanch.com](http://trs.akakanch.com)项目的源代码。包括了前端和后端。前端主要以JavaScript为主。后端主要以Python为主。Python版本为Python3.5

什么是成信助手？

> 一个出于个人一时兴趣做的网站,目前拥有以下功能：

> __成信好老师__：从老师的教学风格，严格程度等方面评价老师。任何评价都有可能成为日后其它学生选课的依据。

>__成信贴吧大数据__：可以对我们学校的贴吧进行一些简单的分析，包括用户维度和贴吧维度的分析。

>__成信曝光台__：说出对学校(或老师或同学或学校周边黑心商家)的不满。赢取更大关注，争取公平公正。



如果你对该份代码有任何问题，请联系：[kanch@akakanch.com](kanch@akakanch.com)

**【若要参与贡献，请访问issues页面】**

理论上讲，[该站点（http://cuit.akakanch.com/）](http://cuit.akakanch.com/)会运行到我毕业（2019年）

>######关于Android客户端
原来是想的以客户端形式分发，后来根据@misszhang的建议，做成了Web版本，当时客户端 已经基本完成了。不过现在看来Android客户端已经作废，故同样上传到GitHub上来。

>Android项目需要Android Studio 2.3及以上打开。

---
##文件夹说明

###**【Web】**
>trs/Web/

这里是成信好老师网页的代码包括前端和后端。

（不包括一些API接口）


###**【Utilities - Microsoft Azure App Service】**
 >trs/Utilities - Microsoft Azure App Service/

这里的代码运行在 Azure App Service上，这里主要是用作贴吧大数据的API查询接口，给定用户ID或者我们的一个指定用户编码，可以通过这个API返回用户的关键字，活跃度，活跃时间段。同时该API接口也适用于贴吧短语分析。

（这里的代码同时包括了之前的邮箱查询验证）

###**【Tieba-Crawler】**
>trs/Tieba-Crawler/

这是新版爬虫的源代码（候选），对应 [issue 5](https://github.com/ankanch/cuit-trs/issues/5)。该版本结合一些先进库来完成。并且高度模块化。
（[点击这里查看旧版爬虫](https://github.com/ankanch/tieba-zhuaqu)）


###**【tiebabigdata-user-analyze】**
>trs/tiebabigdata-user-analyze/

这里是用于对贴吧用户进行简单分析的python脚本。

包括 k-means 聚类（余弦相似性），用户关键字提取（通过VSM分类（即将完成）），用户提到的地名/学院提取（用于猜测用户属性）

---

【**已弃用】**【Utilities - OSS】
 >trs/Utilities - OSS/

【不再提供该服务】

这里是负责进行邮件通知新闻更新，检查成信新闻是否有新新闻的服务代码（Python）。

这里的代码运行在另外一个服务器上，主要负责按照一定的频率检测新闻是否更新，更新了的话判断是哪种新闻，然后从数据库获取对应类型的新闻订阅者邮件列表，然后向这些邮件列表发送新闻更新提醒。

【**已弃用】**【Utilities - Google App Engine】
 >trs/Utilities - Google App Engine/

这里是成信新闻的API接口网站的代码（Python）。它主要负责新闻的抓取，已经新闻更新的提醒。但由于国内访问不了Google App Engine，故弃用。

【**已弃用】**【TeacherRating】
>trs/TeacherRating/

这里是旧版本（安卓版）的成信好老师（trs）代码。正如我之前说的，由于网页版更加便捷，故放弃。







---

__该文件更新缓慢__

