from sqlalchemy.orm import sessionmaker

from db.models import engine, Playlist, Track

Session = sessionmaker(bind=engine)


def create_playlist(args):
    name = args['name']

    session = Session()
    new_playlist = Playlist(name=name)
    session.add(new_playlist)
    session.commit()

    if new_playlist.id:
        return new_playlist
    return None


def rename_playlist(args):
    new_name = args['new_name']
    playlist_id = args['playlist_id']

    session = Session()
    playlist = session.query(Playlist).get(playlist_id)
    playlist.name = new_name
    session.commit()

    if playlist.id:
        return playlist
    return None


def delete_playlist(args):
    playlist_id = args['playlist_id']

    session = Session()
    playlist = session.query(Playlist).get(playlist_id)
    session.delete(playlist)
    session.commit()

    return True


def add_track_to_playlist(args):
    track = args['track']
    playlist_id = args['playlist_id']

    session = Session()
    new_track = Track(name=track['name'],
                      duration=track['duration'],
                      artists=track['artists'],
                      youtube_id=track['youtube_id'],
                      playlist_id=playlist_id)
    session.add(new_track)
    session.commit()

    if new_track.id:
        return new_track
    return None


def remove_track(args):
    track_id = args['track_id']

    session = Session()
    my_track = session.query(Track).get(track_id)
    session.delete(my_track)
    session.commit()

    return True
