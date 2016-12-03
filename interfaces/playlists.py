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
    playlists = graphene.List(Playlist)
    tracks = graphene.List(Track)
    playlist = graphene.Field(Playlist, id=graphene.String())

    def resolve_playlists(self, args, context, info):
        query = Playlist.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_tracks(self, args, context, info):
        query = Track.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_playlist(self, args, context, info):
        playlist_id = args['id']
        query = Playlist.get_query(context)  # SQLAlchemy query
        return query.get(playlist_id)


#############
# MUTATIONS #
#############

class CreatePlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlists = graphene.List(lambda: Playlist)

    def mutate(self, args, context, info):
        name = args.get('name')

        new_playlist = handler.create_playlist({'name': name})
        if new_playlist:
            ok = True
        else:
            ok = False

        query = Playlist.get_query(context)
        return CreatePlaylist(playlists=query.all(), ok=ok)


class RenamePlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlists = graphene.List(lambda: Playlist)

    def mutate(self, args, context, info):
        playlist_id = args.get('playlist_id')
        new_name = args.get('new_name')

        playlist = handler.rename_playlist({'playlist_id': playlist_id,
                                            'new_name': new_name})
        if playlist:
            ok = True
        else:
            ok = False

        query = Playlist.get_query(context)
        return RenamePlaylist(playlists=query.all(), ok=ok)


class DeletePlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlists = graphene.List(lambda: Playlist)

    def mutate(self, args, context, info):
        playlist_id = args.get('playlist_id')

        ok = handler.delete_playlist({'playlist_id': playlist_id})
        query = Playlist.get_query(context)
        return DeletePlaylist(playlists=query.all(), ok=ok)


class TrackInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    duration = graphene.String(required=True)
    artists = graphene.String(required=True)
    youtube_id = graphene.String()


class AddTrackToPlaylist(graphene.Mutation):
    ok = graphene.Boolean()
    playlists = graphene.List(lambda: Playlist)

    def mutate(self, args, context, info):
        new_track = args.get('track')
        playlist_id = args.get('playlist_id')

        track = handler.add_track_to_playlist({'playlist_id': playlist_id,
                                               'track': new_track})
        if track:
            ok = True
        else:
            ok = False

        query = Playlist.get_query(context)
        return AddTrackToPlaylist(playlists=query.all(), ok=ok)


class RemoveTrack(graphene.Mutation):
    ok = graphene.Boolean()
    playlists = graphene.List(lambda: Playlist)

    def mutate(self, args, context, info):
        track_id = args.get('track_id')

        ok = handler.remove_track({'track_id': track_id})
        query = Playlist.get_query(context)
        return RemoveTrack(playlists=query.all(), ok=ok)


class Mutation(graphene.ObjectType):
    create_playlist = CreatePlaylist.Field(name=graphene.String())
    rename_playlist = RenamePlaylist.Field(playlist_id=graphene.String(),
                                           new_name=graphene.String())
    delete_playlist = DeletePlaylist.Field(playlist_id=graphene.String())

    add_track = AddTrackToPlaylist.Field(track=TrackInput(),
                                         playlist_id=graphene.String())
    remove_track = RemoveTrack.Field(track_id=graphene.String())


##########
# SCHEMA #
##########

schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
