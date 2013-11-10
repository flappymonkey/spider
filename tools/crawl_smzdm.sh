function usage()
{
    local argv0=$0
    echo $argv0' prd/dev smzdm/etao_smzdm partition_num detect/detectmove'
}
if [ $# -ne 4 ] ; then
    usage $0
    exit -1
fi
if [ $1 == 'prd' ] ; then
    work_path=/home/ops/ToC_2014/
elif [ $1 == 'dev' ] ; then
    work_path=/home/luoy/ToC/
else
    usage $0
    exit -1
fi
partition_num=$3
action=$4
if [ $2 == 'smzdm' ] ; then
    cd $work_path/Spider/Smzdm/ && scrapy crawl SmzdmSpider -a mode=2 && cd $work_path/Spider/tools 
    if [ $? -ne 0 ] ; then
        usage $0
        exit -1
    fi
elif [ $2 == 'etao_smzdm' ] ; then
    cd $work_path/Spider/etao_smzdm/ && scrapy crawl etao_smzdm && cd $work_path/Spider/tools
    if [ $? -ne 0 ] ; then
        usage $0
        exit -1
    fi
else
    usage $0
    exit -1
fi
max_slice=$((partition_num-1))
for slice in `seq 0 $max_slice`
do
    nohup python detect_data.py $action $2 $slice $partition_num >> ../log/detect_data_$2.out 2>&1 &
done
