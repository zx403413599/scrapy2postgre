下载年鉴目录地址
url_down = Request(url = "http://data.cnki.net/Yearbook/PartialNaviResult?code=A&code2=&page=1&pagerow=60000&type=type&type2=", method = "POST")
年鉴标题：/html/body/div[1]/div[1]/div/div/h3/a
年鉴收录年份：/html/body/div[1]/div[1]/div/ul/li[1]/a
	      /html/body/div[1]/div[1]/div/ul
历任主编：/html/body/div[1]/div[1]/div/p[2]
编纂机构：/html/body/div[1]/div[1]/div/p[3]
出版社：/html/body/div[1]/div[1]/div/p[4]



下载固定年鉴目录内容
url_new = Request(url = 'http://data.cnki.net/Yearbook/PartialGetCatalogResult?entrycode=&page=1&pagerow=20000&ybcode=N2014120083',method = 'POST')
条目名称：/html/body/div[2]/table/tbody/tr[4]/td[1]
页码：/html/body/div[2]/table/tbody/tr[4]/td[2]
下载：/html/body/div[2]/table/tbody/tr[4]/td[3]
