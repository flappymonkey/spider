#!/bin/bash
spider_list='qq_yxthh
sn_zq8dd
taobao_jhs
vancl_miaosha
zhe800_baoyou
taobao_tejia
'
workdir=~/ToC/Spider
logdir=$workdir/log
mkdir -p $logdir
check()
{
    local spider=$1
    #ps aux|egrep "sh start_crawl.sh $spider|scrapy crawl $spider|firefox|sleep"|grep -v grep |awk '{print $2}' > .tmp
    ps aux|egrep "sh start_crawl.sh $spider|scrapy crawl $spider"|grep -v grep |awk '{print $2}' > .tmp
    #local pid_list=`ps aux|egrep "sh start_crawl.sh $spider|scrapy crawl $spider|firefox"|grep -v grep |awk '{print $2}'`
    local pid_list=""
    for pid in `cat .tmp`
    do
        pid_list=$pid_list" "$pid
    done
    #local pid_list=`cat .tmp`
    local ps_num=0
    for pid in `echo $pid_list`
    do
        ps_num=$((ps_num+1))
    done
    echo $pid_list
    #echo $ps_num
    return $ps_num
}
check_one()
{
    local spider=$1
    echo -n $spider" "
    check $spider
}
start()
{
    local spider=$1
    check $spider > /dev/null
    local ps_num=$?
    if [ $ps_num -gt 0 ] ; then
        echo "already start $spider"
    else
        nohup sh start_crawl.sh $spider 1>> $logdir/$spider.out 2>>$logdir/$spider.err &
    fi
}
stop()
{
    local spider=$1
    local pid_list=`check $spider`
    for pid in `echo $pid_list`
    do
        kill -9 $pid
    done
}
usage()
{
    echo $0 'check/start/stop'
    for spider in $spider_list
    do
        echo $spider
    done
}
if [ $# -eq 2 ] ; then
    $1 $2
elif [ $# -eq 1 ] ; then
    if [ $1 = 'check_all' ] ; then
        for spider in `echo $spider_list`
        do
            check_one $spider
        done
    elif [ $1 == 'start_all' ] ; then
        for spider in `echo $spider_list`
        do
            start $spider
        done
    elif [ $1 == 'stop_all' ] ; then
        for spider in `echo $spider_list`
        do
            stop $spider
        done
    fi
else
    usage $0
    exit 255
fi
cd $workdir
#for spider in `echo $spider_list`
#do
#    nohup sh start_crawl.sh $spider 1>> $logdir/$spider.out 2>>$logdir/$spider.err &
#done
