"""This is the last.fm API module.

This module search last.fm for songs and artists
and retrieve their metadata.
"""

import pylast
import time

from interfaces import discover


# You have to have your own unique two values for API_KEY and API_SECRET
API_KEY = "4893839b9e0f9ffbd67cbe633a289a43"
API_SECRET = "dacbdf956a17d6ea12d7a2b5bf441c0d"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)


def search_tracks_by_name(track_name, artist_name=""):
    tracks = network.search_for_track(track_name=track_name,
                                      artist_name=artist_name)\
                                      .get_next_page()
    return list(map(process_track, tracks))


def search_tracks_by_artist_name(artist_name):
    t1 = time.time()
    artist = network.get_artist(artist_name=artist_name)
    tracks = artist.get_top_tracks(limit=10)
    t2 = time.time()
    print("lasfm api time: " + str(t2-t1))
    print(tracks)
    t1 = time.time()
    lst = list(map(process_top_tracks, tracks))
    t2 = time.time()
    print("gql process time: " + str(t2 - t1))
    return lst


def process_track(trk):
    t1 = time.time()
    duration = trk.get_duration()
    t2 = time.time()
    print("lasfm duration time: " + str(t2 - t1))
    return discover.Track(name=trk.title,
                          duration=duration,
                          artists=trk.artist.name)


def process_top_tracks(top_trk):
    return process_track(top_trk.item)


# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works
