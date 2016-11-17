# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

from scrapy2postgre.items import zbfl


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["http://data.stats.gov.cn"]
    start_urls = (
        #年度数据
        'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=hgnd&wdcode=zb&m=getTree',
    )

    def parse(self, response):
        """解析指标分类，
        先创建一个item，
        然后将返回的内容设置解码格式，
        然后将解码后的内容放置到item中，
        判断是不是父分类，
        如果是，则继续解析指标分类，
        如果不是则解析返回内容
        为保证后续爬取数据时分省和不分省的数据可以采用同一个链接，
        查询结果的行采用zb。列采用sj，查询条件为地区和时间范围，
        条件均放在dfwds中。
        """
        zbfls = json.loads(response.body_as_unicode())
        fldata = zbfl()
        for fl in zbfls:
            fldata["dbcode"] = fl["dbcode"]
            fldata["code"] = fl["id"]
            fldata["isParent"] = fl["isParent"]
            fldata["name"] = fl["name"]
            fldata["pid"] = fl["pid"]
            fldata["wdcode"] = fl["wdcode"]
            yield fldata
            if fl['isParent']:
                url_next = 'http://data.stats.gov.cn/easyquery.htm?id=' + fl['id'] + '&dbcode=' + fl[ \
                    'dbcode'] + '&wdcode=zb&m=getTree'
                yield Request(url_next, callback=self.parse)