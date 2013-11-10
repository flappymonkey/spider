list="Z秒杀
聚划算
易迅
苏宁易购
凡客
淘宝
天天特价
一淘
"
category_list="穿的
吃的
数码/家电
日用品
化妆品
其它
"
function usage()
{
    local argv0=$1
    echo $argv0 " debug_mode = 1 or 0"
}
if [ $# -ne 1 ] ; then
    usage $0
    exit -1
fi
debug_mode=$1
host=localhost
port=27017
if [ $debug_mode -eq 1 ] ; then
    db_name=scrapy_test
    table=scrapy_info
else
    db_name=seckills
    table=seckill
fi
function show_db()
{
    local db_name=$1
    local table=$2
    local has_category=$3
    date_str=`date +"%Y-%m-%d %H:%M:%S"`
    if [ $has_category -gt 0 ] ; then
        for source in `echo $list`
        do
                echo -n $date_str" "$source" "
                echo 'db.'$table'.find({"source": "'$source'"}).count()'|mongo $host:$port/$db_name|egrep -v '^MongoDB|connecting|bye'
                for cat in `echo $category_list`
                do
                        date_str=`date +"%Y-%m-%d %H:%M:%S"`
                        echo -n $date_str" "$source" "$cat" "
                        echo 'db.'$table'.find({"category_name": "'$cat'", "source":"'$source'"}).count()'|mongo $host:$port/$db_name|egrep -v '^MongoDB|connecting|bye'
                done
        done
        for source in `echo $category_list`
        do
            echo -n $date_str" "$source" "
            echo 'db.'$table'.find({"category_name": "'$source'"}).count()'|mongo $host:$port/$db_name|egrep -v '^MongoDB|connecting|bye'
        done
    fi
    if [ $has_category -gt 1 ] ; then
        for source in `echo $list`
        do
            echo -n $date_str" "$db_name" "$table" "$source" "
            echo 'db.'$table'.find({"source": "'$source'"}).count()'|mongo $host:$port/$db_name|egrep -v '^MongoDB|connecting|bye'
        done
    fi
    echo -n $date_str" "$db_name" "$table" "total" "
    echo 'db.'$table'.find().count()'|mongo $host:$port/$db_name|egrep -v '^MongoDB|connecting|bye'
}
while true;
do
        show_db $db_name $table 2
        show_db $db_name old_$table 0
        show_db scrapy ztmhs 0
        show_db scrapy old_ztmhs 0
        sleep 3600
done
