import pytest

from xasd.uploader.track_info import track_info, artist_names


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
