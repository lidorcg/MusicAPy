from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey)
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship)
from sqlalchemy.ext.declarative import declarative_base

# TODO: add artist model
# TODO: add album model
# TODO: add many-to-many track-playlist relation
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tracks = relationship('Track',
                          back_populates='playlist',
                          cascade='all, delete, delete-orphan')


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration = Column(String)
    artists = Column(String)
    # album = Column(String)
    youtube_id = Column(String)
    playlist_id = Column(Integer, ForeignKey('playlist.id'))
    playlist = relationship('Playlist', back_populates='tracks')


# This will create all the tables on the first run
Base.metadata.create_all(bind=engine)
