（1）url分析
医院列表url：https://www.guahao.com/hospital/2/上海/3315/徐汇区/p11
注意：一级行政区和二级行政区必须都有，否者数据获取不全
（2）获取一级行政区和二级行政区名称及ID
一级url：https://www.guahao.com/json/white/area/provinces
二级url：https://www.guahao.com/json/white/area/citys?provinceId=1
