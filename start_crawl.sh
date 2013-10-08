spider=$1
cd $spider
while true ;
do
    scrapy crawl $spider
    sleep 600
done
cd -
