import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from db import handler, models
from providers import spotify_provider, youtube_provider


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
        model = models.MyList


class MyTrack(SQLAlchemyObjectType):
    class Meta:
        model = models.MyTrack


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
    ok = graphene.Boolean()
    list = graphene.Field(lambda: MyList)

    def mutate(self, args, context, info):
        name = args.get('name')

        new_list = handler.create_list({'name': name})
        if new_list:
            ok = True
        else:
            ok = False
        return CreateList(list=new_list, ok=ok)


class RenameList(graphene.Mutation):
    ok = graphene.Boolean()
    list = graphene.Field(lambda: MyList)

    def mutate(self, args, context, info):
        list_id = args.get('list_id')
        new_name = args.get('new_name')

        my_list = handler.rename_list({'list_id': list_id,
                                       'new_name': new_name})
        if my_list:
            ok = True
        else:
            ok = False
        return RenameList(list=my_list, ok=ok)


class DeleteList(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        list_id = args.get('list_id')

        ok = handler.delete_list({'list_id': list_id})
        return DeleteList(ok=ok)


class TrackInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    duration = graphene.String(required=True)
    artists = graphene.String(required=True)
    spotify_id = graphene.String(required=True)
    youtube_id = graphene.String(required=True)


class AddTrack(graphene.Mutation):
    ok = graphene.Boolean()
    track = graphene.Field(lambda: MyTrack)

    def mutate(self, args, context, info):
        new_track = args.get('track')
        list_id = args.get('list_id')

        my_track = handler.add_track({'list_id': list_id,
                                      'track': new_track})
        if my_track:
            ok = True
        else:
            ok = False
        return AddTrack(track=my_track, ok=ok)


class RemoveTrack(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        track_id = args.get('track_id')

        ok = handler.remove_track({'track_id': track_id})
        return RemoveTrack(ok=ok)


class Mutation(graphene.ObjectType):
    create_list = CreateList.Field(name=graphene.String())
    rename_list = RenameList.Field(list_id=graphene.Int(),
                                   new_name=graphene.String())
    delete_list = DeleteList.Field(list_id=graphene.Int())

    add_track = AddTrack.Field(track=TrackInput(),
                               list_id=graphene.Int())
    remove_track = RemoveTrack.Field(track_id=graphene.Int())


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
