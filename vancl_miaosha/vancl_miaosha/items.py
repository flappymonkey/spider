#coding=utf-8

from scrapy.item import Item, Field

class VanclMiaoshaItem(Item):
    # define the fields for your item here like:
    id = Field() #id
    source = Field() #来源
    title = Field() #标题
    link = Field() #商品详情页链接
    img = Field() #图片
    ori_price = Field() #原始价格
    cur_price = Field() #当前价格
    discount = Field() #折扣
    limit = Field() #限额，没有设置为0
    sale = Field() #销售额
    sale_percent = Field() #销售比例
    display_time_begin = Field() #显示开始时间
    display_time_end = Field() #显示结束时间
    actual_time_begin = Field() #实际开始时间
    actual_time_end = Field() #实际失效时间
    stat = Field() #已失效，进行中，即将开始
