"""This is the Youtube API module.

This module search youtube for the requested song
and returns the id of it's video.
"""

from apiclient.discovery import build


DEVELOPER_KEY = "AIzaSyCK8R2WVOHFCZGurocP9zAEwic_U2PGlKc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_track_id(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    res = youtube.search().list(
        q=query,
        part='id',
        type="video",
        videoCategoryId="10",
        maxResults="1"
    ).execute()

    return res['items'][0]['id']['videoId']
