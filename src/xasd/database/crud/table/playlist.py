import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Playlist as PlaylistModel
from xasd.database.models import Track as TrackModel


class Playlist(Table):
    table = PlaylistModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = PlaylistModel.name

    def add_track_to_playlist(self, playlist_id, track_id, user_id):
        """Add a track to a playlist

        Args:
            playlist_id (int): Playlist id
            track_id (int): Track id
            user_id (int): User id
        """
        playlist = self.get(
            filter=[
                PlaylistModel.playlist_id == playlist_id
                and PlaylistModel.user_id == user_id
            ],
        )
        track = self.get(table=TrackModel, filter=[TrackModel.track_id == track_id])

        playlist.tracks.append(track)
        self._session.commit()

        return playlist

    def remove_track_from_playlist(self, playlist_id, track_id, user_id):
        """Remove a track from a playlist

        Args:
            playlist_id (int): Playlist id
            track_id (int): Track id
            user_id (int): User id
        """
        playlist = self.get(
            filter=[
                PlaylistModel.playlist_id == playlist_id
                and PlaylistModel.user_id == user_id
            ],
        )
        track = self.get(table=TrackModel, filter=[TrackModel.track_id == track_id])
        playlist.tracks.remove(track)
        self._session.commit()

        return playlist
