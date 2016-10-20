import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from db import handler, models


##########
# MODELS #
##########


class Playlist(SQLAlchemyObjectType):
    class Meta:
        model = models.Playlist


class Track(SQLAlchemyObjectType):
    class Meta:
        model = models.Track


##############
# ROOT QUERY #
##############

class Query(graphene.ObjectType):
    all_playlists = graphene.List(Playlist)
    all_tracks = graphene.List(Track)

    def resolve_all_playlists(self, args, context, info):
        query = Playlist.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_all_tracks(self, args, context, info):
        query = Track.get_query(context)  # SQLAlchemy query
        return query.all()


#############
# MUTATIONS #
#############

class CreatePlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlist = graphene.Field(lambda: Playlist)

    def mutate(self, args, context, info):
        name = args.get('name')

        new_playlist = handler.create_playlist({'name': name})
        if new_playlist:
            ok = True
        else:
            ok = False
        return CreatePlaylist(playlist=new_playlist, ok=ok)


class RenamePlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlist = graphene.Field(lambda: Playlist)

    def mutate(self, args, context, info):
        playlist_id = args.get('playlist_id')
        new_name = args.get('new_name')

        playlist = handler.rename_playlist({'playlist_id': playlist_id,
                                            'new_name': new_name})
        if playlist:
            ok = True
        else:
            ok = False
        return RenamePlaylist(playlist=playlist, ok=ok)


class DeletePlaylist(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        playlist_id = args.get('playlist_id')

        ok = handler.delete_playlist({'playlist_id': playlist_id})
        return DeletePlaylist(ok=ok)


class TrackInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    duration = graphene.String(required=True)
    artists = graphene.String(required=True)
    spotify_id = graphene.String(required=True)
    youtube_id = graphene.String(required=True)


class AddTrack(graphene.Mutation):
    ok = graphene.Boolean()
    track = graphene.Field(lambda: Track)

    def mutate(self, args, context, info):
        new_track = args.get('track')
        playlist_id = args.get('playlist_id')

        track = handler.add_track({'playlist_id': playlist_id,
                                   'track': new_track})
        if track:
            ok = True
        else:
            ok = False
        return AddTrack(track=track, ok=ok)


class RemoveTrack(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        track_id = args.get('track_id')

        ok = handler.remove_track({'track_id': track_id})
        return RemoveTrack(ok=ok)


class Mutation(graphene.ObjectType):
    create_list = CreatePlaylist.Field(name=graphene.String())
    rename_list = RenamePlaylist.Field(playlist_id=graphene.Int(),
                                       new_name=graphene.String())
    delete_list = DeletePlaylist.Field(playlist_id=graphene.Int())

    add_track = AddTrack.Field(track=TrackInput(),
                               playlist_id=graphene.Int())
    remove_track = RemoveTrack.Field(track_id=graphene.Int())


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
