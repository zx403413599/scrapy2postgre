增加中国知网统计年鉴目录内容爬取，爬取统计年鉴数据的内容介绍。
=================================================================
完成一个版本的编制，近期暂停爬虫的相关工作，除非需要接入新的数据源。
开始完成c数据查询的相关功能。
增加定时任务计划，每周一爬取一次。
写了一个dos脚本。
内容如下：
d:
cd D:\projects\scrapy2postgre1.1
activate scrapy && scrapy crawl test --loglevel=ERROR
=====================================================
2016年11月17日
1、本工程是statdata工程里面数据爬取子功能的1.1版本。
2、相比那个版本已经实现了将数据爬取到postgresql数据库中。
3、丰富完代码注释后，暂时封版1.0
4、下一个小版本要增加爬虫处理统计局网站的另外一种形式的数据，即Excel文件数据。
