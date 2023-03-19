def test_read_playlists_me(create_playlist, client):
    token = create_playlist["token"]
    response = client.get("/playlist/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
        "playlists": [
            {
                "name": "playlist_name",
                "playlist_id": 1,
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
    }


def test_create_playlist(create_token, client):
    response = client.post(
        "/playlist",
        json={"name": "playlist_name"},
        headers={"Authorization": f"Bearer {create_token}"},
    )
    assert response.status_code == 201
    assert response.json() == {"name": "playlist_name", "playlist_id": 1, "tracks": []}


def test_options_playlist(client):
    response = client.options("/playlist")
    assert response.status_code == 200
    assert response.headers == {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "OPTIONS, POST",
        "access-control-allow-headers": "accept, Authorization",
        "content-length": "0",
    }


def test_add_track_to_playlist(create_playlist, client):
    token = create_playlist["token"]
    response = client.patch(
        "/playlist/1/track/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "playlist_name",
        "playlist_id": 1,
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


# # def test_remove_track_from_playlist(create_playlist, client):
