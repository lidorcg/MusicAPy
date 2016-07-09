"""This is the Spotify API module.

This module search spotify for songs and artists
and retrieve their metadata.
"""

import spotipy


sp = spotipy.Spotify()


def search_tracks(q):
    return sp.search(q=q, limit=20, type='track')['tracks']['items']


def search_artists(q):
    return sp.search(q=q, limit=4, type='artist')['artists']['items']


def get_track(track_id):
    return sp.track(track_id)


def get_artist(artist_id):
    return sp.artist(artist_id)


def get_artist_top_tracks(artist_id):
    return sp.artist_top_tracks(artist_id)['tracks']
