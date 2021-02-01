from marshmallow import fields, Schema, post_load

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
    def __init__(self, spotify_id: str, spotify_url: str, title: str, images: list, artists: list, rating: int, listened_to: bool):
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


if __name__ == "__main__":
    images = [
            {
                "height" : 640,
                "url" : "https://i.scdn.co/image/ab67616d0000b273674c2b8b77e1e9259a2fcb87",
                "width" : 640
            },
            {
                "height" : 300,
                "url" : "https://i.scdn.co/image/ab67616d00001e02674c2b8b77e1e9259a2fcb87",
                "width" : 300
            },
            {
                "height" : 64,
                "url" : "https://i.scdn.co/image/ab67616d00004851674c2b8b77e1e9259a2fcb87",
                "width" : 64
            }
        ]

    artists = [
        {
            "name": "Radiohead",
            "spotify_url": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb"
        }
    ]

    album_data = {
        "spotify_id": "6GjwtEZcfenmOf6l18N7T7",
        "spotify_url": "https://open.spotify.com/album/6GjwtEZcfenmOf6l18N7T7",
        "title": "Kid A",
        "images": images,
        "artists": artists,
        "rating": 0,
        "listened_to": False
    }

    schema = AlbumSchema()
    result = schema.load(album_data)

    print(schema.dump(result))