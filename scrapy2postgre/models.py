from sqlalchemy import create_engine,Column,Integer,NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from scrapy.conf import settings

DeclarativeBase = declarative_base()

def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return create_engine(URL(**settings.DATABASE))

def create_tables(engine):
    """"create tables as define of class below"""
    DeclarativeBase.metadata.create_all(engine)

class zbfl(DeclarativeBase):
    __tablename__ = "zbfl"

    id = Column(Integer, primary_key=True)

#
# class zbmeta(DeclarativeBase):
#     __tablename__ = "zb"
#
#     id = Column(Integer, primary_key=True)
#
#
# class regmeta(DeclarativeBase):
#     __tablename__ = "reg"
#
#     id = Column(Integer,primary_key=True)
#
# class sjmeta(DeclarativeBase):
#     __tablename__ = "sj"
#
#     id = Column(Integer, primary_key=True)
#
# class zbdata(DeclarativeBase):
#     __tablename__ = "zbdata"
#
#     id = Column(Integer, primary_key=True)