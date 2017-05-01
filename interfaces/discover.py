import graphene
from providers import lastfm, spotify, youtube


# TODO: connect track model with artist model
# TODO: add album model


##########
# MODELS #
##########

class Track(graphene.ObjectType):
    name = graphene.String()
    duration = graphene.String()
    artists = graphene.String()
    youtube_id = graphene.String()

    def resolve_youtube_id(self, args, context, info):
        return youtube.get_track_id(self.artists, self.name, self.duration)


class Artist(graphene.ObjectType):
    name = graphene.String()
    tracks = graphene.List(lambda: Track)
    images = graphene.List(lambda: Image)
    spotify_id = graphene.String()

    def resolve_images(self, args, context, info):
        return spotify.get_artist_images(self.spotify_id)

    def resolve_tracks(self, args, context, info):
        return spotify.get_artist_top_tracks(self.spotify_id)


class Image(graphene.ObjectType):
    width = graphene.String()
    height = graphene.String()
    url = graphene.String()


##############
# ROOT QUERY #
##############

class Query(graphene.ObjectType):
    search_tracks_spotify = graphene.List(Track, query=graphene.String())
    search_artists_spotify = graphene.List(Artist, query=graphene.String())
    search_tracks_by_name_lastfm = \
        graphene.List(Track,
                      artist_name=graphene.String(),
                      track_name=graphene.String())
    search_tracks_by_artist_name_lastfm = \
        graphene.List(Track, artist_name=graphene.String())

    def resolve_search_tracks_spotify(self, args, context, info):
        return spotify.search_tracks(args['query'])

    def resolve_search_artists_spotify(self, args, context, info):
        return spotify.search_artists(args['query'])

    def search_tracks_by_track_name_lastfm(self, args, context, info):
        return lastfm.search_tracks_by_name(args['track_name'],
                                            args['artist_name'])

    def resolve_search_tracks_by_artist_name_lastfm(self, args, context, info):
        return lastfm.search_tracks_by_artist_name(args['artist_name'])


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,)
