from marshmallow import fields, Schema, post_load
from datetime import datetime
import boto3
import uuid

# Artist
class Artist:
    def __init__(self, name: str, spotify_url: str):
        self.name = name
        self.spotify_url = spotify_url


class ArtistSchema(Schema):
    name = fields.Str()
    spotify_url = fields.Str()

    @post_load
    def create_artist(self, data, **kwargs):
        return Artist(**data)


# Album Cover
class AlbumCover:
    def __init__(self, height: int, width: int, url: str):
        self.height = height
        self.width = width
        self.url = url


class AlbumCoverSchema(Schema):
    height = fields.Int()
    width = fields.Int()
    url = fields.Str()

    @post_load
    def create_album_cover(self, data, **kwargs):
        return AlbumCover(**data)


# Album
class Album:
    def __init__(
        self,
        spotify_id: str,
        spotify_url: str,
        title: str,
        images: list,
        artists: list,
        rating: int,
        listened_to: bool,
    ):
        self.spotify_id = spotify_id
        self.spotify_url = spotify_url
        self.title = title
        self.images = images
        self.artists = artists
        self.rating = rating
        self.listened_to = listened_to


class AlbumSchema(Schema):
    spotify_id = fields.Str()
    spotify_url = fields.Str()
    title = fields.Str()
    images = fields.List(fields.Nested(AlbumCoverSchema))
    artists = fields.List(fields.Nested(ArtistSchema))
    rating = fields.Int()
    listened_to = fields.Bool()

    @post_load
    def create_album(self, data, **kwargs):
        return Album(**data)


class ListenList:
    def __init__(
        self,
        list_id: str,
        owner_id: str,
        created_at: str,
        updated_at: str,
        list_title: str,
        albums: list,
    ):
        self.list_id = list_id
        self.owner_id = owner_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.list_title = list_title
        self.albums = albums
    
    def add_album(self, album: Album):
        """Adds an album object to the the list of albums

        Args:
            album (Album): An album.
        """
        if album.spotify_id not in [a.spotify_id for a in self.albums]:
            self.albums.append(album)
        else:
            print(f"{album.title} is already in this list.")

    def remove_albums(self, album_ids: list):
        """Removes an album based on the ID

        Args:
            album_id (str): The id of the album to remove
        """
        updated_albums = [album for album in self.albums if album.spotify_id not in album_ids]
        self.albums = updated_albums
    
    def store(self):
        """Stores the ll in dynamo
        """
        print('Saving List')
        schema = ListenListSchema()
        item = schema.dump(self)
        db = boto3.resource("dynamodb")
        table = db.Table("ListenList")
        response = table.put_item(Item=item)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return item
        return False

    def delete(self):
        """Deletes the ll from dynamo
        """
        key = {
            "list_id": self.list_id,
        }
        db = boto3.resource("dynamodb")
        table = db.Table("ListenList")
        response = table.delete_item(Key=key)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print('Deleted List')
            return True
        return False

class ListenListSchema(Schema):
    list_id = fields.Str()
    owner_id = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    list_title = fields.Str()
    albums = fields.List(fields.Nested(AlbumSchema))

    @post_load
    def create_ll(self, data, **kwargs):
        return ListenList(**data)


if __name__ == "__main__":
    pass