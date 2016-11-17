from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()

def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return create_engine("postgresql://postgres:ximen120@localhost/scrapy2postgre",pool_size=2000, max_overflow=30,pool_timeout = 600)


def create_tables(engine):
    """"create tables as define of class below"""
    DeclarativeBase.metadata.create_all(engine)

class zbfl(DeclarativeBase):
    __tablename__ = "zbfl"

    dbcode = Column(String(200))
    code = Column(String(200))
    isParent = Column(Boolean)
    name = Column(String(200))
    pid = Column(String(200))
    wdcode = Column(String(200))
    id = Column(Integer, primary_key=True)

class zbdata(DeclarativeBase):
    __tablename__ = "zbdata"

    id = Column(Integer, primary_key=True)
    dbcode =  Column(String(200))
    code =  Column(String(200))
    data =  Column(String(200))
    dotcount =  Column(Integer)
    hasdata =  Column(Boolean)
    strdata =  Column(String(200))
    # 指标外键
    zb_valuecode =  Column(String(200))
    zb_wdcode =  Column(String(200))
    # 时间外键
    sj_valuecode =  Column(String(200))
    sj_wdcode =  Column(String(200))
    # 地区外键
    reg_valuecode =  Column(String(200))
    reg_wdcode =  Column(String(200))

# 定义指标class
class zbmeta(DeclarativeBase):
    __tablename__ = "zbmeta"

    id = Column(Integer, primary_key=True)
    dbcode =  Column(String(200))
    wdcode =  Column(String(200))
    wdname =  Column(String(200))
    cname =  Column(String(2000))
    code =  Column(String(200))
    dotcount =  Column(Integer)
    exp =  Column(String(2000))
    ifshowcode =  Column(Boolean)
    memo =  Column(String(2000))
    name =  Column(String(2000))
    nodesort =  Column(Integer)
    sortcode =  Column(Integer)
    tag =  Column(String(2000))
    unit =  Column(String(200))

# 定义指标class
class regmeta(DeclarativeBase):
    __tablename__ = "regmeta"

    id = Column(Integer, primary_key=True)
    dbcode = Column(String(200))
    wdcode = Column(String(200))
    wdname = Column(String(200))
    cname = Column(String(2000))
    code = Column(String(200))
    dotcount = Column(Integer)
    exp = Column(String(2000))
    ifshowcode = Column(Boolean)
    memo = Column(String(2000))
    name = Column(String(2000))
    nodesort = Column(Integer)
    sortcode = Column(Integer)
    tag = Column(String(2000))
    unit = Column(String(200))


# 定义指标class
class sjmeta(DeclarativeBase):
    __tablename__ = "sjmeta"

    id = Column(Integer, primary_key=True)
    dbcode = Column(String(200))
    wdcode = Column(String(200))
    wdname = Column(String(200))
    cname = Column(String(2000))
    code = Column(String(200))
    dotcount = Column(Integer)
    exp = Column(String(2000))
    ifshowcode = Column(Boolean)
    memo = Column(String(2000))
    name = Column(String(2000))
    nodesort = Column(Integer)
    sortcode = Column(Integer)
    tag = Column(String(2000))
    unit = Column(String(200))