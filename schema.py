import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import MyList as MyListModel, MyTrack as MyTrackModel
import db_mutator
import spotify_api
import youtube_api


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
        query = youtube_query_builder(self.artists, self.name)
        return youtube_api.get_track_id(query)


class Artist(graphene.ObjectType):
    name = graphene.String()
    tracks = graphene.List(lambda: Track)
    images = graphene.List(lambda: Image)
    spotify_id = graphene.String()

    def resolve_images(self, args, context, info):
        images_json = spotify_api.get_artist(self.spotify_id)['images']
        return list(map(process_image, images_json))

    def resolve_tracks(self, args, context, info):
        tracks_json = spotify_api.get_artist_top_tracks(self.spotify_id)
        return list(map(process_track, tracks_json))


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
        tracks_json = spotify_api.search_tracks(args['query'])
        return list(map(process_track, tracks_json))

    def resolve_search_artists(self, args, context, info):
        artists_json = spotify_api.search_artists(args['query'])
        return list(map(process_artist, artists_json))

    def resolve_track(self, args, context, info):
        track_json = spotify_api.get_track(args['id'])
        return process_track(track_json)

    def resolve_artist(self, args, context, info):
        artist_json = spotify_api.get_artist(args['id'])
        return process_artist(artist_json)


#############
# MUTATIONS #
#############

class CreateList(graphene.Mutation):
    class Input:
        name = graphene.String()

    ok = graphene.Boolean()
    list = graphene.Field(lambda: MyList)

    def mutate(self, args, context, info):
        my_list = db_mutator.add_list(MyListModel(name=args.get('name')))
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
        my_track = db_mutator.add_track(new_track)
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


#####################
# utility functions #
#####################

def youtube_query_builder(artists, track_name):
    artists_names = ", ".join(map(lambda a: a.name, artists))
    return '{} {} Lyrics'.format(artists_names, track_name)


def process_track(trk):
    artists = list(map(process_artist, trk['artists']))
    return Track(name=trk['name'],
                 duration=trk['duration_ms'],
                 artists=artists,
                 spotify_id=trk['id'])


def process_artist(art):
    return Artist(name=art['name'], spotify_id=art['id'])


def process_image(img):
    return Image(width=img['width'], height=img['height'], url=img['url'])
