# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import zbfl as model_fl, db_connect, create_tables,zbdata as model_data,zbmeta as model_zb,regmeta as model_reg,sjmeta as model_sj
from scrapy2postgre.items import zbfl as item_fl,zbdata as item_data,zbmeta as item_zb


class Scrapy2PostgrePipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker.
               Creates deals table.
       `"""
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item,spider):
        session = self.Session()
        def count_insert(item, item_name,session):

            def insert(q,data):
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

            if item_name == 'item_fl':
                data = model_fl(**item)
                q = session.query(model_fl).filter(model_fl.dbcode == data.dbcode, model_fl.code == data.code)
                insert(q,data)
            elif item_name == 'item_data':
                data = model_data(**item)
                q = session.query(model_data).filter(model_data.dbcode == data.dbcode, model_data.code == data.code)
                insert(q, data)
            elif item_name == 'item_zb':
                if item["wdcode"] == "zb":
                    data = model_zb(**item)
                    q = session.query(model_zb).filter(model_zb.dbcode == data.dbcode, model_zb.code == data.code)
                    insert(q, data)
                elif item["wdcode"] == 'reg':
                    data = model_reg(**item)
                    q = session.query(model_reg).filter(model_reg.dbcode == data.dbcode, model_reg.code == data.code)
                    insert(q, data)
                elif item["wdcode"] == 'sj':
                    data = model_sj(**item)
                    q = session.query(model_sj).filter(model_sj.dbcode == data.dbcode, model_sj.code == data.code)
                    insert(q, data)


        if isinstance(item,item_fl):
            count_insert(item=item, item_name='item_fl',session=session)
        elif isinstance(item,item_data):
            count_insert(item, item_name='item_data',session=session)
        elif isinstance(item,item_zb):
            count_insert(item,item_name='item_zb',session=session)


