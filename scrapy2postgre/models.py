from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

"""通过sqlachemy库，利用models管理数据库的表结构。
   这样的好处是在切换数据库的时候改变的比较少。
   初衷因为是一个资料中是这样使用的。
"""

DeclarativeBase = declarative_base()

#创建数据库链接，这里的数据库链接字符串是手动拼的，应该是使用URL函数，从settings中的参数拼接。
#但有问题没有解决，这里直接拼接了
def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    #除了拼接数据库链接字符串外，设置了数据池相关的参数，默认值太小，会常导致出错。
    return create_engine("postgresql://postgres:ximen120@localhost/scrapy2postgre", pool_size=2000, max_overflow=30,pool_timeout = 600)

#创建和维护数据库表。
def create_tables(engine):
    """"create tables as define of class below"""
    DeclarativeBase.metadata.create_all(engine)

#定义数据库表的model， 设置一个表名和列名以及列属性。
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

#年鉴信息
class njml(DeclarativeBase):
    __tablename__ = "njml"

    id = Column(Integer, primary_key=True)
    njfl = Column(String(200))
    njid = Column(String(200))
    njname = Column(String(200))
    year_num = Column(Integer)
    njzb = Column(String(2000))
    bzjg = Column(String(2000))
    cbs = Column(String(2000))

#年鉴年份信息
class njnf(DeclarativeBase):
    __tablename__ = "njnf"

    id = Column(Integer, primary_key=True)
    njid = Column(String(200))
    njname = Column(String(200))
    year = Column(String(200))
    year_id = Column(String(2000))

#年鉴目录
class njcontent(DeclarativeBase):
    __tablename__ = "njcontent"

    id = Column(Integer, primary_key=True)
    njid = Column(String(200))
    year_id = Column(String(2000))
    row_count = Column(Integer)
    mlmc = Column(String(2000))
    ym = Column(String(2000))
    filename = Column(String(2000))
    pg = Column(String(200))
    disk = Column(String(2000))
    down_url = Column(String(2000))