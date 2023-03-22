import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Playlist as PlaylistModel
from xasd.database.models import Track as TrackModel


class Playlist(Table):
    table = PlaylistModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = PlaylistModel.name

    def add_track_to_playlist(self, playlist, track):
        """Add a track to a playlist

        Args:
            playlist (PlaylistModel): Playlist
            track (TrackModel): Track

        Returns:
            PlaylistModel: Playlist
        """
        playlist.tracks.append(track)
        self._session.commit()

        return playlist

    def remove_track_from_playlist(self, playlist, track):
        """Remove a track from a playlist

        Args:
            playlist (PlaylistModel): Playlist
            track (TrackModel): Track

        Returns:
            PlaylistModel: Playlist
        """
        playlist.tracks.remove(track)
        self._session.commit()

        return playlist
