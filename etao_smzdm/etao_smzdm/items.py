#coding=utf-8

from scrapy.item import Item, Field

class EtaoSmzdmItem(Item):
    # define the fields for your item here like:
    id = Field() #id
    crawl_source = Field() #crawl source
    source_url = Field()  #source url
    source = Field() # laiyuan
    title = Field()  #title
    desc = Field()   #desc list
    link_desc = Field()   #flag = 1 use
    link = Field()   #flag = 1 use
    desc_link_list = Field() #flag = 0 use
    go_link = Field() #flag = 0 use
    img = Field()    #img list
    cat = Field()    #cat list
    pub_time = Field()  #time
    worth_num = Field() # worth person
    bad_num = Field() # bad person
    flag = Field()
    stat = Field() #0:new 1:use 2:delete
    need_filter = Field() #是否需要判断失效
    same_id = Field() #none表示没有相同的id

