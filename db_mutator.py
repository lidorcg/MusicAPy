from sqlalchemy.orm import sessionmaker
from models import engine, MyList, MyTrack

Session = sessionmaker(bind=engine)


def add_list(new_list):
    session = Session()
    session.add(new_list)
    session.commit()
    if new_list.id:
        return new_list
    return None


def add_track(new_track):
    session = Session()
    session.add(new_track)
    session.commit()
    if new_track.id:
        return new_track
    return None
