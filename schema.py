import graphene
import spotify_api
import youtube_api


class Track(graphene.ObjectType):
    spotify_id = graphene.String()
    name = graphene.String()
    duration = graphene.String()
    artists = graphene.List('Artist')
    youtube_id = graphene.String()

    def resolve_youtube_id(self, args, info):
        query = query_builder(self.artists, self.name)
        return youtube_api.get_track_id(query)


class Image(graphene.ObjectType):
    width = graphene.String()
    height = graphene.String()
    url = graphene.String()


class Artist(graphene.ObjectType):
    spotify_id = graphene.String()
    name = graphene.String()
    images = graphene.List(Image)
    tracks = graphene.List(Track)

    def resolve_images(self, args, info):
        images_json = spotify_api.get_artist(self.spotify_id)['images']
        return list(map(process_image, images_json))

    def resolve_tracks(self, args, info):
        tracks_json = spotify_api.get_artist_top_tracks(self.spotify_id)
        return list(map(process_track, tracks_json))


class Query(graphene.ObjectType):
    search_tracks = graphene.List(Track, query=graphene.String())
    search_artists = graphene.List(Artist, query=graphene.String())
    track = graphene.Field(Track, id=graphene.String())
    artist = graphene.Field(Artist, id=graphene.String())

    def resolve_search_tracks(self, args, info):
        tracks_json = spotify_api.search_tracks(args['query'])
        return list(map(process_track, tracks_json))

    def resolve_search_artists(self, args, info):
        artists_json = spotify_api.search_artists(args['query'])
        return list(map(process_artist, artists_json))

    def resolve_track(self, args, info):
        track_json = spotify_api.get_track(args['id'])
        return process_track(track_json)

    def resolve_artist(self, args, info):
        artist_json = spotify_api.get_artist(args['id'])
        return process_artist(artist_json)


schema = graphene.Schema(query=Query)


# utility functions
def query_builder(artists, track_name):
    artists_names = ", ".join(map(lambda a: a.name, artists))
    return '{} {} Lyrics'.format(artists_names, track_name)


def process_track(trk):
    artists = list(map(process_artist, trk['artists']))
    return Track(spotify_id=trk['id'], name=trk['name'], duration=trk['duration_ms'], artists=artists)


def process_artist(art):
    return Artist(spotify_id=art['id'], name=art['name'])


def process_image(img):
    return Image(width=img['width'], height=img['height'], url=img['url'])
