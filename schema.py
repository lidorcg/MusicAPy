import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import MyList as MyListModel, MyTrack as MyTrackModel
from providers import spotify_provider, db_provider, youtube_provider


##########
# MODELS #
##########

class Track(graphene.ObjectType):
    name = graphene.String()
    duration = graphene.String()
    artists = graphene.List(lambda: Artist)
    spotify_id = graphene.String()
    youtube_id = graphene.String()

    def resolve_youtube_id(self, args, context, info):
        return youtube_provider.get_track_id(self.artists, self.name)


class Artist(graphene.ObjectType):
    name = graphene.String()
    tracks = graphene.List(lambda: Track)
    images = graphene.List(lambda: Image)
    spotify_id = graphene.String()

    def resolve_images(self, args, context, info):
        return spotify_provider.get_artist_images(self.spotify_id)

    def resolve_tracks(self, args, context, info):
        return spotify_provider.get_artist_top_tracks(self.spotify_id)


class Image(graphene.ObjectType):
    width = graphene.String()
    height = graphene.String()
    url = graphene.String()


class MyList(SQLAlchemyObjectType):
    class Meta:
        model = MyListModel


class MyTrack(SQLAlchemyObjectType):
    class Meta:
        model = MyTrackModel


##############
# ROOT QUERY #
##############

class Query(graphene.ObjectType):
    my_lists = graphene.List(MyList)
    my_tracks = graphene.List(MyTrack)
    search_tracks = graphene.List(Track, query=graphene.String())
    search_artists = graphene.List(Artist, query=graphene.String())
    track = graphene.Field(Track, id=graphene.String())
    artist = graphene.Field(Artist, id=graphene.String())

    def resolve_my_lists(self, args, context, info):
        query = MyList.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_my_tracks(self, args, context, info):
        query = MyTrack.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_search_tracks(self, args, context, info):
        return spotify_provider.search_tracks(args['query'])

    def resolve_search_artists(self, args, context, info):
        return spotify_provider.search_artists(args['query'])

    def resolve_track(self, args, context, info):
        return spotify_provider.get_track(args['id'])

    def resolve_artist(self, args, context, info):
        return spotify_provider.get_artist(args['id'])


#############
# MUTATIONS #
#############

class CreateList(graphene.Mutation):
    class Input:
        name = graphene.String()

    ok = graphene.Boolean()
    list = graphene.Field(lambda: MyList)

    def mutate(self, args, context, info):
        my_list = db_provider.add_list(MyListModel(name=args.get('name')))
        if my_list:
            ok = True
        else:
            ok = False
        return CreateList(list=my_list, ok=ok)


class AddTrack(graphene.Mutation):
    class Input:
        name = graphene.String()
        duration = graphene.String()
        artists = graphene.String()
        spotify_id = graphene.String()
        youtube_id = graphene.String()
        list_id = graphene.Int()

    ok = graphene.Boolean()
    track = graphene.Field(lambda: MyTrack)

    def mutate(self, args, context, info):
        new_track = MyTrackModel(name=args.get('name'),
                                 duration=args.get('duration'),
                                 artists=args.get('artists'),
                                 spotify_id=args.get('spotify_id'),
                                 youtube_id=args.get('youtube_id'),
                                 list_id=args.get('list_id'))
        my_track = db_provider.add_track(new_track)
        if my_track:
            ok = True
        else:
            ok = False
        return AddTrack(track=my_track, ok=ok)


class Mutation(graphene.ObjectType):
    create_list = CreateList.Field()
    add_track = AddTrack.Field()


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
