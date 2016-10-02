from sqlalchemy.orm import sessionmaker

from db.models import engine, MyList, MyTrack

Session = sessionmaker(bind=engine)


def create_list(args):
    name = args['name']

    session = Session()
    new_list = MyList(name=name)
    session.add(new_list)
    session.commit()

    if new_list.id:
        return new_list
    return None


def rename_list(args):
    new_name = args['new_name']
    list_id = args['list_id']

    session = Session()
    my_list = session.query(MyList).get(list_id)
    my_list.name = new_name
    session.commit()

    if my_list.id:
        return my_list
    return None


def delete_list(args):
    list_id = args['list_id']

    session = Session()
    my_list = session.query(MyList).get(list_id)
    session.delete(my_list)
    session.commit()

    return True


def add_track(args):
    track = args['track']
    list_id = args['list_id']

    session = Session()
    new_track = MyTrack(name=track['name'],
                        duration=track['duration'],
                        artists=track['artists'],
                        spotify_id=track['spotify_id'],
                        youtube_id=track['youtube_id'],
                        list_id=list_id)
    session.add(new_track)
    session.commit()

    if new_track.id:
        return new_track
    return None


def remove_track(args):
    track_id = args['track_id']

    session = Session()
    my_track = session.query(MyTrack).get(track_id)
    session.delete(my_track)
    session.commit()

    return True
