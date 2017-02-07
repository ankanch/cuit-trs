#成信助手#

这里是 [成信助手](http://trs.akakanch.com)的贴吧大数据贴吧用户分析脚本。
主要包括了用户关键字分析和用户活跃时间段分析。以及用户聚类分析。


如果你对该份代码有任何问题，请联系：[kanch@akakanch.com](kanch@akakanch.com)

**【若要参与贡献，请访问issues页面】**

---
##文件说明

###**【TimeZoneAnalyzsis.py】**

用户活跃时间段分析

###**【TimeZoneClassify】**

根据用户的活跃时间段进行k-means聚类（k=3）。

###**【keyword4eachuseroftieba.py】**

用户关键词分析

###**【QueryFunctions.py】**
 >trs/Web/datasourceconfig/

基本的数据库操作函数

###**【locations.txt，schools.txt】**
 >trs/Web/templates/

这里存放了基本的地理位置信息和学院信息，方便用户分类

---

__该文件更新缓慢__

---
【k-means用户活跃时间段聚类分析结果】

#####聚类前的全体数据

![聚类前的全体数据](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/all.png)

#####去除极端值（>400）

![去除极端值（>400）](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/less400-9.png)

#####3个簇的平均活跃时间段

![3个簇的平均活跃时间段](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/2cr1.png)

#####簇1

![簇1](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/2c1.png)

#####簇2

![簇2](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/2c2.png)


#####簇3

![簇3](https://github.com/ankanch/cuit-trs/blob/master/tiebabigdata-user-analyze/Data/result/2c3.png)
