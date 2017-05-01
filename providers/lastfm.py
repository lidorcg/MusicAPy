import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
API_KEY = "4893839b9e0f9ffbd67cbe633a289a43"
API_SECRET = "dacbdf956a17d6ea12d7a2b5bf441c0d"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

# use this function to search tracks by artists
print("####################### SEARCH BY ARTIST NAME #######################")
ARTIST_NAME = "גיא ויהל"
artist = network.get_artist(artist_name=ARTIST_NAME)
print(artist.get_top_tracks())

# use this function to search tracks by name
print("####################### SEARCH BY TRACK NAME #######################")
TRACK_NAME = "השמש תזרח"
tracks = network.search_for_track(artist_name="", track_name=TRACK_NAME)
print(tracks.get_next_page())

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works
