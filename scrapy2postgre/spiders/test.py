# -*- coding: utf-8 -*-
import scrapy
from scrapy2postgre.items import zbfl#zbdata,zbfl,zbmeta,regmeta,sjmeta

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["data.stats.gov.cn"]
    start_urls = (
        'http://www.data.stats.gov.cn/',
    )

    def parse(self, response):
        zbfl["id"]=1
        yield zbfl
