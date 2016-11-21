# -*- coding: utf-8 -*-
import scrapy


class ZgzwSpider(scrapy.Spider):
    name = "zgzw"
    allowed_domains = ["data.cnki.net"]
    start_urls = (
        'http://www.data.cnki.net/',
    )

    def parse(self, response):
        pass
