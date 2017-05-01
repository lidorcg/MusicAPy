"""This is the Youtube API module.

This module search youtube for the requested song
and returns the id of it's video.
"""

from apiclient.discovery import build
import dateutil.parser
from datetime import datetime, date
from functools import reduce

# Read in the file containing the authorization token.
f = open("./developer-key")
dk = f.read()
# Get rid of leading and trailing whitespace.
dk = dk.strip()
f.close()


DEVELOPER_KEY = dk
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def get_track_id(artists, track, duration):
    query = query_builder(artists, track)

    search_response = youtube_search(query)

    videos_ids = map(lambda itm: itm["id"]["videoId"],
                     search_response.get("items", []))

    videos_response = youtube_videos_details(videos_ids)

    best_match = find_best_match(videos_response, duration)

    return best_match['id']


#######################
# auxiliary functions #
#######################


def query_builder(artists, track):
    return '{} {} Lyrics'.format(artists, track)


def youtube_search(query):
    return youtube.search().list(
        q=query,
        part='id',
        type="video",
        videoCategoryId="10",
        maxResults="10"
        ).execute()


def youtube_videos_details(videos_ids):
    return youtube.videos().list(
        id=",".join(videos_ids),
        part='contentDetails'
        ).execute()


def find_best_match(videos_response, duration):
    # TODO: find better match for hebrew
    if duration == 0:
        return videos_response['items'][1]
    # convert duration from millisecond string to time object
    time_duration = datetime.utcfromtimestamp(int(duration) / 1000).time()
    # convert duration from PTMXXSXX string to time object
    videos_with_time_obj = map(parse_yt_time, videos_response.get("items", []))
    # map each id to time delta
    videos_with_time_delta = map((lambda x: map_time_delta(x, time_duration)),
                                 videos_with_time_obj)
    # find item with minimum delta
    best_match = reduce(min_delta, videos_with_time_delta)

    return best_match


def parse_yt_time(item):
    iso_duration = item['contentDetails']['duration']
    time_duration = dateutil.parser.parse(iso_duration[2:]).time()
    return {'id': item['id'], 'duration': time_duration}


def map_time_delta(item, duration):
    delta = abs(datetime.combine(date.today(), item['duration']) -
                datetime.combine(date.today(), duration))
    return {'id': item['id'], 'delta': delta}


def min_delta(itm1, itm2):
    if(itm1['delta'] > itm2['delta']):
        return itm2
    else:
        return itm1
