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


def test_read_playlists_me_no_token(env, client):
    response = client.get("/playlist/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_playlists_me_invalid_token(env, client):
    response = client.get(
        "/playlist/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_playlists_me_no_playlists(create_token, client):
    response = client.get(
        "/playlist/me", headers={"Authorization": f"Bearer {create_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"playlists": []}


def test_create_playlist(create_token, client):
    response = client.post(
        "/playlist",
        json={"name": "playlist_name"},
        headers={
            "Authorization": f"Bearer {create_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"name": "playlist_name", "playlist_id": 1, "tracks": []}


def test_create_playlist_no_name(create_token, client):
    response = client.post(
        "/playlist",
        json={},
        headers={"Authorization": f"Bearer {create_token}"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_create_playlist_no_token(client):
    response = client.post("/playlist", json={"name": "playlist_name"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_playlist_invalid_token(client):
    response = client.post(
        "/playlist",
        json={"name": "playlist_name"},
        headers={"Authorization": f"Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_options_playlist(client):
    response = client.options("/playlist")
    assert response.status_code == 200
    assert response.headers == {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "OPTIONS, POST, PATCH, DELETE",
        "access-control-allow-headers": "accept, Authorization, Content-Type",
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


def test_add_track_to_playlist_no_token(env, client):
    response = client.patch("/playlist/1/track/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_add_track_to_playlist_invalid_token(env, client):
    response = client.patch(
        "/playlist/1/track/1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_add_track_to_playlist_nonexistent(create_token, client):
    response = client.patch(
        "/playlist/1/track/1", headers={"Authorization": f"Bearer {create_token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}


def test_add_track_to_playlist_no_track(create_playlist, client):
    token = create_playlist["token"]
    response = client.patch(
        "/playlist/1/track/999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Track not found"}


def test_remove_track_from_playlist(create_playlist, client):
    # add track to playlist
    token = create_playlist["token"]
    response = client.patch(
        "/playlist/1/track/1", headers={"Authorization": f"Bearer {token}"}
    )

    # remove track from playlist
    response = client.delete(
        "/playlist/1/track/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "playlist_name",
        "playlist_id": 1,
        "tracks": [],
    }


def test_remove_track_from_playlist_no_token(env, client):
    response = client.delete("/playlist/1/track/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_remove_track_from_playlist_invalid_token(env, client):
    response = client.delete(
        "/playlist/1/track/1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_remove_track_from_playlist_nonexistent(create_token, client):
    response = client.delete(
        "/playlist/1/track/1", headers={"Authorization": f"Bearer {create_token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}


def test_remove_track_from_playlist_no_track(create_playlist, client):
    token = create_playlist["token"]
    response = client.delete(
        "/playlist/1/track/999", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Track not found"}


def test_delete_playlist(create_playlist, client):
    token = create_playlist["token"]
    response = client.delete(
        "/playlist/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    assert response.content == b""


def test_delete_playlist_no_token(env, client):
    response = client.delete("/playlist/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_playlist_invalid_token(env, client):
    response = client.delete(
        "/playlist/1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_playlist_nonexistent(create_token, client):
    response = client.delete(
        "/playlist/1", headers={"Authorization": f"Bearer {create_token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}


def test_update_playlist(create_playlist, client):
    token = create_playlist["token"]
    response = client.patch(
        "/playlist",
        json={"name": "new_playlist_name", "playlist_id": 1, "tracks": []},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "new_playlist_name",
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
