# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["data.stats.gov.cn"]
    start_urls = (
        'http://www.data.stats.gov.cn/',
    )

    def parse(self, response):
        pass
