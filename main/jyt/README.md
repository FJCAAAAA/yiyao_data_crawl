####################京药通app 送药上门 数据爬取####################

一、调研问题及解决方法

    问题1：请求url中携带加密参数 sign
    解决方法1：Xposed+Inspeckage

二、接口分析

1.原始接口

    ###药品类目
    http://ydapi.yjj.beijing.gov.cn/basicinfo/sbasicInfoAction!comboxTreeByParam.do?paramValue=YPYTFL
    ###药品列表
    http://ydapi.yjj.beijing.gov.cn/storedrugrel/storedrugrelRefAction!searchDrugList.do?appKey=hxkey2019&searchKey=&drugType=01&pageIndex=1&pageSize=10&timestamp=1578299510760&sign=cdc55e373edf78507fc85ce02e1174fd
    ###药品详情
    http://ydapi.yjj.beijing.gov.cn/storedrugrel/storedrugrelRefAction!getDrugInfoById.do?appKey=hxkey2019&longitude=116.570066&latitude=39.791684&drugId=73170a59c3e111e99d48801844edb918&userId=&storeId=&timestamp=1578299558536&sign=a6a5c85529a84a43e756a52fe58b7af9

2.各接口的可变参数

    ###药品列表：drugType, pageIndex, timestamp, sign
    ###药品详情：drugId, timestamp, sign

3.加密算法

    使用36位MD5加密，具体被加密字串为（{}为占位符）：
    ###药品列表：appKey=hxkey2019&drugType={}&pageIndex={}&pageSize=10&timestamp={}
    ###药品详情：appKey=hxkey2019&drugId={}&latitude=39.791684&longitude=116.570066&timestamp={}

三、数据爬取

1.分页

    使用滚动分页，准确页数无法定位，需要根据返回数据中 data 字段是否为空判断分页已经完成。
