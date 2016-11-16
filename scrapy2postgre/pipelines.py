# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import zbfl,db_connect,create_tables #zbdata,zbmeta,regmeta,sjmeta,


class Scrapy2PostgrePipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker.
               Creates deals table.
       `"""
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()

        #分类的处理
        fl_item = item[""]+item[""]
        fl = zbfl(**fl_item)
        try:
            session.add(fl)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        #
        # #指标的处理
        # zb_item = item[""]+item[""]
        # zb = zbmeta(**zb_item)
        # try:
        #     session.add(zb)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        #
        # #地区的处理
        # reg_item = item[""]+item[""]
        # reg = regmeta(**reg_item)
        # try:
        #     session.add(reg)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        #
        # #时间的处理
        # sj_item = item[""]+item[""]
        # sj = sjmeta(**sj_item)
        # try:
        #     session.add(sj)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()


        #指标数据的处理
        data_item = item[""]+item[""]
        data = zbdata(**data_item)
        try:
            session.add(data)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
