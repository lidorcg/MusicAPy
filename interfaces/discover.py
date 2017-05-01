import graphene
from providers import spotify, youtube


# TODO: connect track model with artist model
# TODO: add album model


##########
# MODELS #
##########

class Track(graphene.ObjectType):
    name = graphene.String()
    duration = graphene.String()
    artists = graphene.String()
    spotify_id = graphene.String()
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
    search_tracks = graphene.List(Track, query=graphene.String())
    search_artists = graphene.List(Artist, query=graphene.String())
    track = graphene.Field(Track, id=graphene.String())
    artist = graphene.Field(Artist, id=graphene.String())

    def resolve_search_tracks(self, args, context, info):
        return spotify.search_tracks(args['query'])

    def resolve_search_artists(self, args, context, info):
        return spotify.search_artists(args['query'])

    def resolve_track(self, args, context, info):
        return spotify.get_track(args['id'])

    def resolve_artist(self, args, context, info):
        return spotify.get_artist(args['id'])


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,
    )
