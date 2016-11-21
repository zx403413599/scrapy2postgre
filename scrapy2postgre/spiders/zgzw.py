# -*- coding: utf-8 -*-
import scrapy

from scrapy2postgre.items import njnf,njml,njcontent

class ZgzwSpider(scrapy.Spider):
    name = "zgzw"

    def start_requests(self):
        urls = [
            # 统计年鉴
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=A&code2=&page=1&pagerow=6000&type=type&type2=',
            # 分析报告
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=B&code2=&page=1&pagerow=6000&type=type&type2=',
            # 资料汇编
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=C&code2=&page=1&pagerow=6000&type=type&type2=',
            # 调查资料
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=D&code2=&page=1&pagerow=6000&type=type&type2=',
            # 普查资料
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=E&code2=&page=1&pagerow=6000&type=type&type2=',
            # 统计摘要
            'http://data.cnki.net/Yearbook/PartialNaviResult?code=F&code2=&page=1&pagerow=6000&type=type&type2=',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,method='POST')


    def parse(self, response):
        njxx = njml()
        nj_fl = {'A':'统计年鉴','B':'分析报告','C':'资料汇编','D':'调查资料','E':'普查资料','F':'统计摘要'}
        nj_fl_key = response.url.split('?')[1].split('&')[0].split('=')[1]
        njxx["njfl"] = nj_fl[nj_fl_key]
        nj_count = len(response.selector.xpath('//div[@class="Y_tit clearfix"]'))
        for i in range(nj_count):
            njxx["njid"] = response.selector.xpath('//div[@class="Y_tit clearfix"]/h3/a/@href').extract()[i].split('/')[3]
            njxx["njname"] = response.selector.xpath('//div[@class="Y_tit clearfix"]/h3/a/text()').extract()[i]
            njxx["njzb"] = response.selector.xpath('//div[@class="Y_nav_tit fl"]/p[2]/text()').extract()[i]
            njxx["bzjg"] = response.selector.xpath('//div[@class="Y_nav_tit fl"]/p[3]/text()').extract()[i]
            njxx["cbs"] = response.selector.xpath('//div[@class="Y_nav_tit fl"]/p[4]/text()').extract()[i]
            year_path = '//div[@id = "ResultList"]/div['+ str(i+1) +']/div/ul/li'
            njxx["year_num"] = len(response.selector.xpath(year_path))
            yield  njxx
            for j in range(1,njxx["year_num"]+1):
                njyear = njnf()
                njyear["njid"] = njxx["njid"]
                njyear["njname"] = njxx["njname"]
                yearname_path = year_path+'['+str(j)+']'
                year_ml = response.selector.xpath(yearname_path+'/a/text()').extract()
                year_id = response.selector.xpath(yearname_path+'/a/@href').extract()
                for key,year in zip(year_ml,year_id):
                    njyear["year"] = key
                    njyear["year_id"] = year.split('/')[3]
                    yield njyear
                    url_new = "http://data.cnki.net/Yearbook/PartialGetCatalogResult?entrycode=&page=1&pagerow=200000&ybcode="\
                                + njyear["year_id"]
                    yield scrapy.Request(url=url_new, callback=self.parse_content, method='POST',\
                                         meta={'njid': njyear["njid"],'year_id': njyear["year_id"]})

    def parse_content(self, response):
        """解析年鉴具体目录"""
        njnr = njcontent()
        njnr["njid"] = response.meta['njid']
        njnr["year_id"] = response.meta['year_id']
        count = len(response.selector.xpath('/html/body/div[2]/table/tr'))
        for i in range(2,count+1):
            path = '/html/body/div[2]/table/tr['+str(i)+']'
            njnr["row_count"] = i-1
            if len(response.selector.xpath(path+'/td[1]/a/span'))==1:
                njnr["mlmc"] = '    '+response.selector.xpath(path + '/td[1]/a/span/text()').extract()[0]
            else:
                njnr["mlmc"] = response.selector.xpath(path+'/td[1]/a/text()').extract()[0]
            njnr["ym"] = response.selector.xpath(path+'/td[2]/text()').extract()[0]
            njnr["filename"] = response.selector.xpath(path+'/td[3]/a/@fn').extract()[0]
            njnr["pg"] = response.selector.xpath(path+'/td[3]/a/@pg').extract()[0]
            njnr["disk"] = response.selector.xpath(path+'/td[3]/a/@disk').extract()[0]
            if len(response.selector.xpath(path+'/td[3]/a'))>1:
                njnr["down_url"] = response.selector.xpath(path+'/td[3]/a[2]/@href').extract()[0]
            yield njnr