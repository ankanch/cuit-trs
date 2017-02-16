## 贴吧爬虫2

---
#### 这里的爬虫停止更新，请移步[贴吧爬虫2repo:https://github.com/ankanch/tieba-crawler](https://github.com/ankanch/tieba-crawler)

---

这里为改良版的贴吧爬虫，第一个版本参见[tieba-zhuaqu](https://github.com/ankanch/tieba-zhuaqu).

 这个版本的爬虫使用了`BeautifulSoup4` 和`多线程`。采用`高度模块化`的设计。加上一个`易于配置的配置文件`。简化贴吧回帖数据抓取任务。

---
### 与一个版本相比

该版本非分布式爬虫。无分布爬虫调度。

---
### 如果你要成功运行，需要确保以下步骤完成：

* 确保已经安装 BeautifulSoup4 模块。Python版本为Python3
* 确保`Config/systemrelatedenv.py`里面的`AGV_EXE_ENV_LINUX`配置项已经设置为相应的操作系统
* 确保`Config`文件夹已经成功添加用于数据库的数据库配置文件`database.py`(请参见Config文件夹的README)
* 确保`targetTieba.py`里已经正确设置贴吧名
* 在以上设置全都通过后，请直接运行`main.py`即可

---
### 文件夹以及文件说明



 > Cache 缓存文件夹，存放下载的网页以及待插入数据库的数据

 > Config 爬虫配置文件，包括数据库，脚本的配置

 > Crawler 下载网页的爬虫脚本

 > Parser 从网页中提取数据的脚本

 > Worker 用于协调任务的worker，包括下载，匹配，数据库事务。

 > main.py 爬虫的入口文件，请直接运行该文件

 > targetTieba.py 目标贴吧设置文件，在这里配置要抓取的贴吧

 > dbconflicts.txt 数据库冲突日志，提交失败的数据库命令存放在这里

---
### 其它

在GPL协议下您可以自由修改源代码

![GPL](https://camo.githubusercontent.com/0e71b2b50532b8f93538000b46c70a78007d0117/68747470733a2f2f7777772e676e752e6f72672f67726170686963732f67706c76332d3132377835312e706e67)