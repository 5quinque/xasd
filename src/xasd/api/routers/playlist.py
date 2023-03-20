from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from xasd.api import dependencies

from xasd.database import models, schemas


playlist_router = APIRouter(
    prefix="/playlist",
    tags=["Playlist"],
    # dependencies=[Depends(db)],
    responses={404: {"description": "Not found"}},
)


# get users lists of playlists
@playlist_router.get("/me", response_model=schemas.PlaylistList)
async def read_playlists_me(current_user: dependencies.current_user):
    if current_user:
        return {"playlists": current_user.playlists}

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


# create a new playlist for the current user
@playlist_router.post("/", response_model=schemas.Playlist, status_code=201)
async def create_playlist(
    playlist: schemas.PlaylistCreate,
    current_user: dependencies.current_user,
    db: dependencies.database,
):
    if current_user:
        return db.playlist.create(
            filter=[
                models.Playlist.name == playlist.name
                and models.Playlist.user_id == current_user.id
            ],
            name=playlist.name,
            owner_id=current_user.user_id,
        )

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


# preflight options req for /playlist
@playlist_router.options("/", response_model=schemas.Playlist)
async def options_playlist():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST",
            "Access-Control-Allow-Headers": "accept, Authorization",
        }
    )


# add a track to a playlist for the current user
@playlist_router.patch(
    "/{playlist_id}/track/{track_id}",
    response_model=schemas.Playlist,
    status_code=201,
)
async def add_track_to_playlist(
    playlist_id: int,
    track_id: int,
    current_user: dependencies.current_user,
    db: dependencies.database,
):
    if current_user:
        playlist = db.playlist.get(filter=[models.Playlist.playlist_id == playlist_id])
        if not playlist or playlist.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found",
            )

        track = db.track.get(filter=[models.Track.track_id == track_id])
        if not track:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track not found",
            )

        return db.playlist.add_track_to_playlist(
            playlist_id=playlist_id,
            track_id=track_id,
            user_id=current_user.user_id,
        )

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


# remove a track from a playlist for the current user
@playlist_router.delete(
    "/{playlist_id}/track/{track_id}",
    response_model=schemas.Playlist,
    status_code=201,
)
async def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    current_user: dependencies.current_user,
    db: dependencies.database,
):
    if current_user:
        playlist = db.playlist.get(filter=[models.Playlist.playlist_id == playlist_id])
        if not playlist or playlist.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found",
            )

        track = db.track.get(filter=[models.Track.track_id == track_id])
        if not track:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track not found",
            )

        return db.playlist.remove_track_from_playlist(
            playlist_id=playlist_id,
            track_id=track_id,
            user_id=current_user.user_id,
        )

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


# delete playlist for the current user
@playlist_router.delete(
    "/{playlist_id}",
    status_code=204,
)
async def delete_playlist(
    playlist_id: int,
    current_user: dependencies.current_user,
    db: dependencies.database,
):
    if current_user:
        playlist = db.playlist.get(filter=[models.Playlist.playlist_id == playlist_id])
        if not playlist or playlist.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Playlist not found",
            )
        playlist = db.playlist.get(filter=[models.Playlist.playlist_id == playlist_id])
        db.playlist.delete(playlist)
        return Response(status_code=204)

    raise HTTPException(
        status_code=401,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
