####################饿了么app 送药上门 数据爬取####################
一、调研问题及解决方法

    问题1：饿了么app采用了SSL pinning，经过Charles代理后，app会出现网络异常现象，无法正常使用。
    解决方法1：Xposed+JustTrustMe，使用Xposed框架手机需要ROOT，这里使用的是 夜神模拟器。
    问题2：app可以登陆了，并且能看到首页，但是在首页点击 送药上门 模块时app会出现闪退现象，无法看到门店及商品。
    解决方法2：借助第三方工具 AddSecurityExceptionAndroid，给apk增加了允许https抓包的配置。
    参考：https://book.crifan.com/books/app_capture_package_tool_charles/website/how_capture_app/complex_https/https_ssl_pinning/

二、接口分析
1.原始接口如下：

    ###门店列表
    https://newretail.ele.me/newretail/main/shoplist?cat_id=0&channel=health&device_id=c0283e66-a339-3b3e-822f-0eff62a9fb95&fromalipay=0&pn=1&rn=10&rule_id=0&scene_id=0&scene_type=shop&sortby=&type=1&user_type=auto&window=3&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533&city_id=3
    ###类别列表
    https://newretail.ele.me/newretail/shop/getshopcategoryinfo?shop_id=1929623455&sku_id=&device_id=c0283e66-a339-3b3e-822f-0eff62a9fb95&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533&city_id=3
    ###商品列表
    https://newretail.ele.me/newretail/shop/getfoodsbycategory?category_id=157681817007395,157629069307179,15549738030616&shop_id=1929623455&type=1&device_id=c0283e66-a339-3b3e-822f-0eff62a9fb95&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533&city_id=3
    ###商品详情
    https://newretail.ele.me/newretail/shop/getgoodsdetail?plat=bdwm&shop_id=1929623455&sku_id=15761149840794355&device_id=c0283e66-a339-3b3e-822f-0eff62a9fb95&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533&city_id=3
    ###商品说明书
    https://newretail.ele.me/newretail/drug/getupcdruginfos?upc_ids=1514845866&device_id=EFFF1F4DD0044588AFC6600CA010A265%7C1576636493209&lng=116.562972&lat=39.786675&shardlocation=116.562972,39.786675&city_id=3
2.经尝试，device_id和city_id两个参数是不需要的，调整如下：

    ###门店列表
    https://newretail.ele.me/newretail/main/shoplist?cat_id=0&channel=health&fromalipay=0&pn=1&rn=10&rule_id=0&scene_id=0&scene_type=shop&sortby=&type=1&user_type=auto&window=3&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533
    ###类别列表
    https://newretail.ele.me/newretail/shop/getshopcategoryinfo?shop_id=1929623455&sku_id=&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533
    ###商品列表
    https://newretail.ele.me/newretail/shop/getfoodsbycategory?category_id=157681817007395,157629069307179,15549738030616&shop_id=1929623455&type=1&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533
    ###商品详情
    https://newretail.ele.me/newretail/shop/getgoodsdetail?plat=bdwm&shop_id=1929623455&sku_id=15761149840794355&lng=116.56297199428082&lat=39.78667499497533&shardlocation=116.56297199428082,39.78667499497533
    ###商品说明书
    https://newretail.ele.me/newretail/drug/getupcdruginfos?upc_ids=1514845866&lng=116.562972&lat=39.786675&shardlocation=116.562972,39.786675
    需要注意的是，并不是所有商品都有说明书，没有说明书的商品（例如：汤臣倍健）需要查看 商品详情 的response的description、illustration字段
3.各接口的可变参数

    ###门店列表：lng、lat、shardlocation
    ###类别列表：shop_id、lng、lat、shardlocation
    ###商品列表：category_id、shop_id、type、lng、lat、shardlocation
    ###商品详情：shop_id、sku_id、lng、lat、shardlocation
    ###商品说明书：upc_ids、lng、lat、shardlocation
    除了经纬度，其他参数都可以从上次的response获得

三、数据爬取
1.经纬度

    经过对比，饿了么经纬度和腾讯地图经纬度匹配度较高，所以采用腾讯地图接口获取经纬度。
2.选址

    一线、二线、三线、四线、五线城市，每个城市20个小区
