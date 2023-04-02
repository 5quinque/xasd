def test_search_any_nonexistent(env, client):
    with client as c:
        response = c.get("/search/any/non_existent_query")
    assert response.status_code == 200
    assert response.json() == {"albums": [], "artists": [], "tracks": []}


def test_search_any(create_track, client):
    with client as c:
        response = c.get("/search/any/track_title")
    assert response.status_code == 200
    assert response.json() == {
        "tracks": [
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
        ],
        "albums": [],
        "artists": [],
    }


def test_search_track_nonexistent(env, client):
    with client as c:
        response = c.get("/search/track/non_existent_query")
    assert response.status_code == 200
    assert response.json() == []


def test_search_track(create_track, client):
    with client as c:
        response = c.get("/search/track/track_title")

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
