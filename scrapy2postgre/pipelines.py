# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import zbfl as model_fl, db_connect, create_tables #zbdata,zbmeta,regmeta,sjmeta,
from scrapy2postgre.items import zbfl as item_fl


class Scrapy2PostgrePipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker.
               Creates deals table.
       `"""
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item,spider):
        if isinstance(item,item_fl):
            fl = model_fl(**item)
            session = self.Session()
            q = session.query(model_fl).filter(model_fl.dbcode == fl.dbcode, model_fl.id == fl.id)
            if not session.query(q.exists()).scalar():
                try:
                    session.add(fl)
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()

            return item
