import pytest

from xasd.downloader.torrent import get_infohash, get_displayname


@pytest.mark.parametrize(
    "magnet_link, expected",
    [
        (
            "magnet:?xt=urn:btih:JU2XD5427C7P6VE7CMNPDZIDQTLV64XB&dn=Fedora-Workstation-Live-aarch64-37&tr=http%3A%2F%2Ftorrent.fedoraproject.org%3A6969%2Fannounce",
            "JU2XD5427C7P6VE7CMNPDZIDQTLV64XB",
        ),
        (
            "magnet:?xt=urn:btih:2d5f2b5b9c1b1e1e1e1e1e1e1e1e1e1e1e1e1e&dn=ubuntu-20.04.1-desktop-amd64.iso",
            "2d5f2b5b9c1b1e1e1e1e1e1e1e1e1e1e1e1e1e",
        ),
    ],
)
def test_get_infohash(magnet_link, expected):
    assert get_infohash(magnet_link) == expected


@pytest.mark.parametrize(
    "magnet_link, expected",
    [
        (
            "magnet:?xt=urn:btih:JU2XD5427C7P6VE7CMNPDZIDQTLV64XB&dn=Fedora-Workstation-Live-aarch64-37&tr=http%3A%2F%2Ftorrent.fedoraproject.org%3A6969%2Fannounce",
            "Fedora-Workstation-Live-aarch64-37",
        ),
        (
            "magnet:?xt=urn:btih:2d5f2b5b9c1b1e1e1e1e1e1e1e1e1e1e1e1e1e&dn=ubuntu-20.04.1-desktop-amd64.iso",
            "ubuntu-20.04.1-desktop-amd64.iso",
        ),
    ],
)
def test_get_displayname(magnet_link, expected):
    assert get_displayname(magnet_link) == expected
