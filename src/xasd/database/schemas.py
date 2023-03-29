"""pydantic models used in fastapi
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    name: str
    email_address: EmailStr


class UserCreate(UserBase):
    plaintext_password: str


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class FileBase(BaseModel):
    filepath: str


class FileCreate(FileBase):
    pass


class File(FileBase):
    file_id: int
    # track: "Track"

    class Config:
        orm_mode = True


class CoverArtBase(BaseModel):
    filepath: str


class CoverArt(CoverArtBase):
    cover_art_id: int
    # album: "Album"

    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    artist_id: int
    # albums: list["Album"]
    # tracks: list[Track]

    class Config:
        orm_mode = True


class GenreBase(BaseModel):
    name: str = None


class Genre(GenreBase):
    genre_id: int

    class Config:
        orm_mode = True


class TrackBase(BaseModel):
    title: str
    tracknumber: str = None
    date: str = None


class TrackCreate(TrackBase):
    file_id: int
    album_id: int
    artist_id: int
    genre_id: int


class Track(TrackBase):
    track_id: int
    file: File
    artist: Artist
    album: "AlbumWithCoverArt"
    genre: Genre = None
    # playlists: list["Playlist"]

    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    name: str
    # artist_id: int


class AlbumCreate(AlbumBase):
    pass


class AlbumWithCoverArt(AlbumBase):
    cover_art: Optional[CoverArt]

    class Config:
        orm_mode = True


class Album(AlbumBase):
    album_id: int
    artist: Artist
    tracks: list[Track]
    cover_art: Optional[CoverArt]

    class Config:
        orm_mode = True


class PlaylistBase(BaseModel):
    name: str


class PlaylistCreate(PlaylistBase):
    pass


class Playlist(PlaylistBase):
    playlist_id: int
    tracks: list[Track]

    class Config:
        orm_mode = True


class PlaylistList(BaseModel):
    playlists: Optional[list[Playlist]]


class SearchListResponse(BaseModel):
    tracks: list[Optional[Track]]
    albums: list[Optional[Album]]
    artists: list[Optional[Artist]]


class HealthCheckResponse(BaseModel):
    status: str
    time: datetime


Track.update_forward_refs()
