# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""建立item用于从json数据中抽取数据并存储到数据库"""

#指标分类的信息
class zbfl(scrapy.Item):
    dbcode = scrapy.Field()
    code = scrapy.Field()
    isParent = scrapy.Field()
    name = scrapy.Field()
    pid = scrapy.Field()
    wdcode = scrapy.Field()

#指标数据的信息。
class zbdata(scrapy.Item):
    dbcode = scrapy.Field()
    code = scrapy.Field()
    data = scrapy.Field()
    dotcount = scrapy.Field()
    hasdata = scrapy.Field()
    strdata = scrapy.Field()
    # 指标外键
    zb_valuecode = scrapy.Field()
    zb_wdcode = scrapy.Field()
    # 时间外键
    sj_valuecode = scrapy.Field()
    sj_wdcode = scrapy.Field()
    # 地区外键
    reg_valuecode = scrapy.Field()
    reg_wdcode = scrapy.Field()

# 定义元数据的class
class zbmeta(scrapy.Item):
    dbcode = scrapy.Field()
    wdcode = scrapy.Field()
    wdname = scrapy.Field()
    cname = scrapy.Field()
    code = scrapy.Field()
    dotcount = scrapy.Field()
    exp = scrapy.Field()
    ifshowcode = scrapy.Field()
    memo = scrapy.Field()
    name = scrapy.Field()
    nodesort = scrapy.Field()
    sortcode = scrapy.Field()
    tag = scrapy.Field()
    unit = scrapy.Field()