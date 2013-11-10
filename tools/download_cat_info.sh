filename=download_cat
function log_info()
{
    date_str=`date +"%Y-%m-%d %H:%M:%S"`
    echo $date_str" "$@
}
for i in `seq 1 2`
do
    file=$filename.$i.zip
    log_info "start to download "$i
    python download_cat_info.py $i $file
    log_info "end to download "$i
    time=`date "+%Y%m%d%H%M%S"`
    if test -d $i ; then
        mv $i $i.$time
    fi
    mkdir -p $i
    log_info "start to unzip "$i
    cd $i
    unzip ../$file
    cd -
    log_info "end to unzip "$i
done
