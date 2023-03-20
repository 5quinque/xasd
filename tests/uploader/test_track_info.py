import pytest

from xasd.uploader.track_info import artist_names, track_info


@pytest.mark.parametrize(
    "artist, expected",
    [
        (
            "artist1",
            ["artist1"],
        ),
        (
            "artist1, artist2",
            ["artist1", "artist2"],
        ),
        (
            "artist1, artist2, artist3",
            ["artist1", "artist2", "artist3"],
        ),
    ],
)
def test_artist_names(artist, expected):
    assert artist_names(artist) == expected


def test_artist_names_no_artist():
    with pytest.raises(TypeError):
        artist_names(None)


def test_artist_names_empty_artist():
    assert artist_names("") == [""]


def test_artist_names_not_string():
    with pytest.raises(TypeError):
        artist_names(123)


# def test_track_info(mp3_file):
#     assert track_info(mp3_file) == {
#         "album": "My Album",
#         "title": "My Song",
#         "artist": "My Artist",
#         "tracknumber": "1",
#         "genre": "Genre",
#         "date": "2023",
#         "hash": None,
#     }
