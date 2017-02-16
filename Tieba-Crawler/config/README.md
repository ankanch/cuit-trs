## 贴吧爬虫2

---

这里为改良版的贴吧爬虫的`配置文件`文件夹

---
### 如果你要成功运行该爬虫：

* 请在该目录建立 database.py 文件，储存数据库配置。文件必要内容如下：

```python
        NAME="数据库名"
        HOST="数据库主机地址"
        USER="这里填入数据库用户名"
        PASSWORD="这里填入数据库密码"
```


* 该爬虫默认工作在linux环境下，如果你要将其部署在Windows环境下，请修改`systemrelatedenv.py`中的`AGV_EXE_ENV_LINUX`为`False`

---
### 文件说明

 > config.py 爬虫基本配置文件（有详细注释）

 > systemrelatedenv.py 系统环境相关配置

 > urls.py 贴吧RUL一些前缀，方便维护

---
### 其它

在GPL协议下您可以自由修改源代码

![GPL](https://camo.githubusercontent.com/0e71b2b50532b8f93538000b46c70a78007d0117/68747470733a2f2f7777772e676e752e6f72672f67726170686963732f67706c76332d3132377835312e706e67)