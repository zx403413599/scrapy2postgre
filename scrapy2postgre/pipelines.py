# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import zbfl as model_fl, db_connect, create_tables,zbdata as model_data,zbmeta as model_zb,regmeta as model_reg,sjmeta as model_sj
from scrapy2postgre.items import zbfl as item_fl,zbdata as item_data,zbmeta as item_zb

"""这里自己按照资料写了一个将数据存储到postgresql数据库的pipline。"""
class Scrapy2PostgrePipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker.
               Creates deals table.
           连接数据库并维护表结构。
       `"""
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        # 判断item的那个item。不同的item数据存储到不同的数据库表。
        if isinstance(item, item_fl):
            data = model_fl(**item)
            q = session.query(model_fl).filter(model_fl.dbcode == data.dbcode, model_fl.code == data.code)
        elif isinstance(item, item_data):
            data = model_data(**item)
            q = session.query(model_data).filter(model_data.dbcode == data.dbcode, model_data.code == data.code)
        elif isinstance(item, item_zb):
            if item["wdcode"] == "zb":
                data = model_zb(**item)
                q = session.query(model_zb).filter(model_zb.dbcode == data.dbcode, model_zb.code == data.code)
            elif item["wdcode"] == 'reg':
                data = model_reg(**item)
                q = session.query(model_reg).filter(model_reg.dbcode == data.dbcode, model_reg.code == data.code)
            elif item["wdcode"] == 'sj':
                data = model_sj(**item)
                q = session.query(model_sj).filter(model_sj.dbcode == data.dbcode, model_sj.code == data.code)

        # 根据查询结果是否存在，判定要不要将数据插入。
        if not session.query(q.exists()).scalar():
            try:
                session.add(data)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        return item