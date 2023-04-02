def test_read_track(create_track, client):
    with client as c:
        response = c.get("/track/1")
    assert response.status_code == 200
    assert response.json() == {
        "title": "track_title",
        "tracknumber": "1",
        "date": "2023",
        "track_id": 1,
        "file": {"filepath": "filepath", "file_id": 1},
        "artist": {"name": "artist_name", "artist_id": 1},
        "album": {"name": "album_name", "cover_art": None},
        "genre": {"name": "genre_name", "genre_id": 1},
    }


def test_read_track_nonexistent(env, client):
    with client as c:
        response = c.get("/track/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Track not found"}


def test_read_tracks(create_track, client):
    with client as c:
        response = c.get("/track/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "track_title",
            "tracknumber": "1",
            "date": "2023",
            "track_id": 1,
            "file": {"filepath": "filepath", "file_id": 1},
            "artist": {"name": "artist_name", "artist_id": 1},
            "album": {"name": "album_name", "cover_art": None},
            "genre": {"name": "genre_name", "genre_id": 1},
        }
    ]


def test_read_file(create_track, client):
    with client as c:
        response = c.get("/track/1/file")
    assert response.status_code == 200
    assert response.json() == {"filepath": "filepath", "file_id": 1}


def test_read_file_nonexistent(env, client):
    with client as c:
        response = c.get("/track/1/file")
    assert response.status_code == 404
    assert response.json() == {"detail": "Track not found"}
