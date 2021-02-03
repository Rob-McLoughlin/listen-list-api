import os, sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
import pytest
import utils
from classes import AlbumSchema


## TEST DATA ##
ll_data = {
    "created_at": "2021-02-03T00:09:23",
    "albums": [
        {
            "listened_to": False,
            "spotify_url": "https://open.spotify.com/album/6GjwtEZcfenmOf6l18N7T7",
            "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/ab67616d0000b273674c2b8b77e1e9259a2fcb87",
                    "width": 640,
                },
                {
                    "height": 300,
                    "url": "https://i.scdn.co/image/ab67616d00001e02674c2b8b77e1e9259a2fcb87",
                    "width": 300,
                },
                {
                    "height": 64,
                    "url": "https://i.scdn.co/image/ab67616d00004851674c2b8b77e1e9259a2fcb87",
                    "width": 64,
                },
            ],
            "spotify_id": "6GjwtEZcfenmOf6l18N7T7",
            "artists": [
                {
                    "name": "Radiohead",
                    "spotify_url": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
                }
            ],
            "title": "Kid A",
            "rating": 0,
        },
        {
            "listened_to": False,
            "spotify_url": "https://open.spotify.com/album/6GjwtEZcfenmOf6l18N7T7",
            "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/ab67616d0000b273674c2b8b77e1e9259a2fcb87",
                    "width": 640,
                },
                {
                    "height": 300,
                    "url": "https://i.scdn.co/image/ab67616d00001e02674c2b8b77e1e9259a2fcb87",
                    "width": 300,
                },
                {
                    "height": 64,
                    "url": "https://i.scdn.co/image/ab67616d00004851674c2b8b77e1e9259a2fcb87",
                    "width": 64,
                },
            ],
            "spotify_id": "6dVIqQ8qmQ5GBnJ9shOYGE",
            "artists": [
                {
                    "name": "Radiohead",
                    "spotify_url": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
                }
            ],
            "title": "Kid A",
            "rating": 0,
        },
    ],
    "updated_at": "2021-02-03T00:09:23",
    "owner_id": "xyz",
    "list_id": "abc-123",
    "list_title": "List Title One",
}

## TESTS ##
def test_create_ll():
    listen_list = utils.ll_create(ll_data)
    assert listen_list
    assert len(listen_list.albums) > 0
    assert listen_list.list_id == "abc-123"


def test_store_ll():
    listen_list = utils.ll_create(ll_data)
    list_id = listen_list.list_id
    assert utils.ll_store(listen_list) != False
    assert utils.get_ll(list_id) != None


def test_album_changes():
    listen_list = utils.ll_create(ll_data)
    new_album = {
        "spotify_id": "2ix8vWvvSp2Yo7rKMiWpkg",
        "spotify_url": "https://open.spotify.com/album/2ix8vWvvSp2Yo7rKMiWpkg",
        "title": "A Moon Shaped Pool",
        "images": [
            {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b273674c2b8b77e1e9259a2fcb87",
                "width": 640,
            },
            {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e02674c2b8b77e1e9259a2fcb87",
                "width": 300,
            },
            {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d00004851674c2b8b77e1e9259a2fcb87",
                "width": 64,
            },
        ],
        "artists": [
            {
                "name": "Radiohead",
                "spotify_url": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
            }
        ],
        "rating": 0,
        "listened_to": False,
    }
    # Add A Moon Shaped Pool to the List
    new_album = AlbumSchema().load(new_album)
    listen_list.add_album(new_album)
    assert 'A Moon Shaped Pool' in [album.title for album in listen_list.albums]

    # Now remove it
    new_album_id = new_album.spotify_id
    listen_list.remove_albums([new_album_id])
    assert 'A Moon Shaped Pool' not in [album.title for album in listen_list.albums]
