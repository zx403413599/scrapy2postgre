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

#年鉴信息
class njml(scrapy.Item):
    njfl = scrapy.Field() #年鉴分类，根据查询入口不同而不同
    njid = scrapy.Field() #年鉴ID，用于查询年鉴年份信息和年间目录信息
    njname = scrapy.Field() #年鉴中文名称
    year_num = scrapy.Field() #包含内容个数
    njzb = scrapy.Field() #历任主编
    bzjg = scrapy.Field() #编纂机构
    cbs = scrapy.Field()  #出版社

#年鉴年份信息
class njnf(scrapy.Item):
    njid = scrapy.Field()#年鉴ID，用于查询年鉴年份信息和年间目录信息
    njname = scrapy.Field()#年鉴中文名称
    year = scrapy.Field() #包含年份名称
    year_id = scrapy.Field() #包含年份ID，用于查询年鉴目录信息。

#年鉴目录
class njcontent(scrapy.Item):
    njid = scrapy.Field()#年鉴ID，用于查询年鉴年份信息和年间目录信息
    year_id = scrapy.Field()#包含年份ID，用于查询年鉴目录信息。
    row_count = scrapy.Field()#行数
    mlmc = scrapy.Field() #条目标题
    ym = scrapy.Field() #所在年鉴页码
    filename = scrapy.Field() #文件名称，在知网中的名字
    pg = scrapy.Field() #pagerange，知网文件参数
    disk = scrapy.Field() #disk，知网文件参数，未知
    down_url = scrapy.Field() #下载地址。只有excel格式文件下载才有