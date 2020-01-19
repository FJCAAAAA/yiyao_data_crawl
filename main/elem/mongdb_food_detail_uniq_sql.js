/**
 * Created by fengjicheng on 2019/12/30.
 */
var url = "mongodb://localhost:27017/medicine";
var db = connect(url);
// 根据upc去重
db.elem_food_by_cate.aggregate(
    [
        //{$match:{type:1,action:3}}, //可以加条件给这里 匹配type=1 action=3 可选
        { //根据upc分组，$group只会返回参与分组的字段，使用$addToSet在返回结果数组中增加_id字段）
            $group: {
                _id: {upc: '$upc'},
                count: {
                    $sum: 1
                },
                dups: {
                    $addToSet: '$_id'
                }
            }
        },
        {
            $match: {
                count: { //（匹配数量大于1的数据
                    $gt: 1
                }
            }
        }
    ],
        {allowDiskUse: true}
)
.forEach( //（使用forEach循环根据_id删除数据）
    function( doc ){
        doc.dups.shift();
        db.elem_food_by_cate.remove(
            {
                _id: {
                    $in: doc.dups
                }
            }
        );
    }
);

