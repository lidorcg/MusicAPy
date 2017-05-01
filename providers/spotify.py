"""This is the Spotify API module.

This module search spotify for songs and artists
and retrieve their metadata.
"""

import spotipy

from interfaces import discover

sp = spotipy.Spotify()


def search_tracks(q):
    tracks_json = sp.search(q=q, limit=20, type='track')['tracks']['items']
    return list(map(process_track, tracks_json))


def search_artists(q):
    artists_json = sp.search(q=q, limit=4, type='artist')['artists']['items']
    return list(map(process_artist, artists_json))


def get_track(track_id):
    track_json = sp.track(track_id)
    return process_track(track_json)


def get_artist(artist_id):
    artist_json = sp.artist(artist_id)
    return process_artist(artist_json)


def get_artist_top_tracks(artist_id):
    tracks_json = sp.artist_top_tracks(artist_id)['tracks']
    return list(map(process_track, tracks_json))


def get_artist_images(artist_id):
    images_json = sp.artist(artist_id)['images']
    return list(map(process_image, images_json))


#####################
# utility functions #
#####################

def process_track(trk):
    artists = ", ".join(map(process_artist, trk['artists']))
    return discover.Track(name=trk['name'],
                          duration=trk['duration_ms'],
                          artists=artists,
                          spotify_id=trk['id'])


def process_artist(art):
    return art['name']


def process_image(img):
    return discover.Image(width=img['width'],
                          height=img['height'],
                          url=img['url'])
