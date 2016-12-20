# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

from scrapy2postgre.items import zbfl, zbmeta as ZbMeta, zbdata as ZbData


class TestSpider(scrapy.Spider):
    """这是statdata工程里爬取统计局数据的爬虫，负责爬去json格式的数据"""
    name = "gjnd" #爬虫的名字
    allowed_domains = ["data.stats.gov.cn"] #爬虫的允许域名
    start_urls = (  #爬虫的种子地址，获取指标分类，然后获取元数据和数据
        # #年度数据
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=hgnd&wdcode=zb&m=getTree',
        # # 季度数据
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=hgjd&wdcode=zb&m=getTree',
        # # 月度数据
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=hgyd&wdcode=zb&m=getTree',
        # # 分省月度
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=fsyd&wdcode=zb&m=getTree',
        # # 分省季度
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=fsjd&wdcode=zb&m=getTree',
        # # 分省年度
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=fsnd&wdcode=zb&m=getTree',
        # # 主要城市月度
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=csyd&wdcode=zb&m=getTree',
        # # 主要国家月度数据
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=gjyd&wdcode=zb&m=getTree',
        # # 三大经济体月度数据
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=gjydsdj&wdcode=zb&m=getTree',
        # # 国际市场月度商品价格
        # 'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=gjydsc&wdcode=zb&m=getTree',
        # 主要国家（地区）年度数据
        'http://data.stats.gov.cn/easyquery.htm?id=zb&dbcode=gjnd&wdcode=zb&m=getTree',
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
        zbfls = json.loads(response.body_as_unicode())  #将返回数据的采用unicode解码
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
                url_next = 'http://data.stats.gov.cn/easyquery.htm?id=' + fl['id'] + '&dbcode=' + fl['dbcode'] + \
                           '&wdcode=zb&m=getTree'
                yield Request(url_next, callback=self.parse)  #如果是父分类，继续爬取子分类。
            else:
                url_other = 'http://data.stats.gov.cn/easyquery.htm?m=getOtherWds&dbcode=' + fl['dbcode'] + \
                            '&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"' + fl['id'] + '"}]'
                yield Request(url_other, self.parse_keywd, meta={'dbcode': fl['dbcode'], 'zbcode': fl['id']})
                #如果不是父分类，则拼接具体的参数，爬入关键信息，为爬取具体的元数据和指标数据准备

    def parse_keywd(self, response):

        """用于分地区数据的查询中解析返回的指标信息
         t['returndata'][0]['nodes'][0]['code']
         主要针对非全国数据，需要三个参数，地区、时间和指标，爬取关键字信息，
         然后根据关键字拼接具体的爬取地址。
        """

        # 字典，用于不同期别数据获取期别数不一致。默认100年数据。
        sj_num = {'hgnd': '100',
                  'hgjd': '400',
                  'hgyd': '1200',
                  'fsyd': '1200',
                  'fsjd': '400',
                  'fsnd': '100',
                  'csyd': '1200',
                  'gjyd': '1200',
                  'gjydsdj': '1200',
                  'gjydsc': '1200',
                  'gjnd': '100',
                  }

        zbkeys = json.loads(response.body_as_unicode())
        dbcode = response.meta['dbcode']
        zbcode = response.meta['zbcode']
        if len(zbkeys['returndata']) == 1:  #说明不含地区关键字，直接拼接指标和时间维度
            url_data0 = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=' +dbcode+ '' \
                         '&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"' + zbcode +\
                        '"},{"wdcode":"sj","valuecode":"LAST'+ sj_num[dbcode] + '"}]&k1=1476974092492'
            yield Request(url_data0, self.parse_meta, meta={'dbcode': dbcode})
        else:
            for zbkey in zbkeys['returndata']:
                if zbkey['issj']:
                    pass
                else:
                    nodes = zbkey['nodes']
                    if nodes == None:
                        break
                    else:
                        for node in nodes:
                            regcode = node['code']  #拼接地址、指标和时间属性。
                            url_data = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=' + dbcode + \
                                       '&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"' + regcode + \
                                       '"}]&dfwds=[{"wdcode":"zb","valuecode":"' + zbcode + '"},{"wdcode":"sj","' \
                                       'valuecode":"LAST' + sj_num[dbcode] + '"}]'
                            # print(url_data)
                            yield Request(url_data, self.parse_meta, meta={'dbcode': dbcode})

    # 以下为处理返回数据的函数
    def parse_meta(self, response):
        # zbresult["returncode"] 是网络返回码，就是http码。
        # zbresult["returndata"]["wdnodes"]是元数据部分。
        # zbresult["returndata"]["datanodes"] 是数据部分。

        zbresult = json.loads(response.body_as_unicode())
        dbcode = response.meta['dbcode']
        # 以下为处理元数据信息
        for meta in zbresult["returndata"]["wdnodes"]:
            if meta["nodes"][0] == None:
                break
            else:  #处理元数据信息，时间、地区和指标的元数据属性一致，因此爬取到到一个item中返回。
                zb = ZbMeta()
                zb["dbcode"] = dbcode
                zb["wdcode"] = meta["wdcode"]
                zb["wdname"] = meta["wdname"]
                for zbmeta in meta["nodes"]:
                    zb["code"] = zbmeta["code"]
                    zb["sortcode"] = zbmeta["sortcode"]
                    zb["ifshowcode"] = zbmeta["ifshowcode"]
                    zb["memo"] = zbmeta["memo"]
                    zb["nodesort"] = zbmeta["nodesort"]
                    zb["tag"] = zbmeta["tag"]
                    zb["cname"] = zbmeta["cname"]
                    zb["dotcount"] = zbmeta["dotcount"]
                    zb["unit"] = zbmeta["unit"]
                    zb["name"] = zbmeta["name"]
                    zb["exp"] = zbmeta["exp"]
                    yield zb

        #处理指标的数据
        for data in zbresult["returndata"]["datanodes"]:
            zbdata = ZbData()
            zbdata["dbcode"] = dbcode
            zbdata["code"] = data["code"]
            zbdata["strdata"] = data["data"]["strdata"]
            zbdata["dotcount"] = data["data"]["dotcount"]
            zbdata["data"] = data["data"]["data"]
            zbdata["hasdata"] = data["data"]["hasdata"]
            for metad in data["wds"]:#建立指标数据与元数据的关联关系。
                if metad["wdcode"] == "zb":
                    zbdata["zb_wdcode"] = metad["wdcode"]
                    zbdata["zb_valuecode"] = metad["valuecode"]
                    continue
                if metad["wdcode"] == "reg":
                    zbdata["reg_wdcode"] = metad["wdcode"]
                    zbdata["reg_valuecode"] = metad["valuecode"]
                    continue
                if metad["wdcode"] == "sj":
                    zbdata["sj_wdcode"] = metad["wdcode"]
                    zbdata["sj_valuecode"] = metad["valuecode"]
                    continue
            # 用于处理没有地区信息的数据，默认为国家。
            if zbdata.__contains__("reg_valuecode"):
                pass
            else:
                zbdata["reg_wdcode"] = "reg"
                zbdata["reg_valuecode"] = "000000"
            yield zbdata