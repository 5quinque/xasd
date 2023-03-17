def test_read_albums(create_track, client):
    response = client.get("/artist/artist_name/albums")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "album_name",
            "artist_id": 1,
            "album_id": 1,
            "artist": {"name": "artist_name", "artist_id": 1},
            "tracks": [
                {
                    "title": "track_title",
                    "tracknumber": "1",
                    "date": "2023",
                    "track_id": 1,
                    "file": {"filepath": "filepath", "file_id": 1},
                    "artist": {"name": "artist_name", "artist_id": 1},
                    "genre": {"name": "genre_name", "genre_id": 1},
                }
            ],
        }
    ]


def test_read_albums_nonexistent(env, client):
    response = client.get("/artist/artist_name/albums")
    assert response.status_code == 200
    assert response.json() == []


def test_read_tracks(create_track, client):
    response = client.get("/artist/artist_name/tracks")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "track_title",
            "tracknumber": "1",
            "date": "2023",
            "track_id": 1,
            "file": {"filepath": "filepath", "file_id": 1},
            "artist": {"name": "artist_name", "artist_id": 1},
            "genre": {"name": "genre_name", "genre_id": 1},
        }
    ]


def test_read_tracks_nonexistent(env, client):
    response = client.get("/artist/artist_name/tracks")
    assert response.status_code == 200
    assert response.json() == []
