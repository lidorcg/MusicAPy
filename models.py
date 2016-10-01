from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class MyList(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class MyTrack(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration = Column(String)
    artists = Column(String)
    # album = Column(String)
    spotify_id = Column(String)
    youtube_id = Column(String)
    list_id = Column(Integer, ForeignKey('list.id'))
    list = relationship(
        MyList,
        backref=backref('tracks', uselist=True, cascade='delete,all'))


# This will create all the tables on the first run
Base.metadata.create_all(bind=engine)
