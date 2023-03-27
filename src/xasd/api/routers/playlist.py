from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from xasd.api import dependencies

from xasd.database import models, schemas


playlist_router = APIRouter(
    prefix="/playlist",
    tags=["Playlist"],
    responses={404: {"description": "Not found"}},
)


# get users lists of playlists
@playlist_router.get("/me", response_model=schemas.PlaylistList)
async def read_playlists_me(current_user: dependencies.current_user):
    return {"playlists": current_user.playlists}


# options req for /playlist/me
@playlist_router.options("/me", response_model=schemas.PlaylistList)
async def options_playlists_me():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, GET",
            "Access-Control-Allow-Headers": "accept, Authorization, Content-Type",
        }
    )


# create a new playlist for the current user
@playlist_router.post("", response_model=schemas.Playlist, status_code=201)
async def create_playlist(
    playlist: schemas.PlaylistCreate,
    current_user: dependencies.current_user,
    db: dependencies.database,
):
    return db.playlist.create(
        filter=[
            models.Playlist.name == playlist.name
            and models.Playlist.user_id == current_user.id
        ],
        name=playlist.name,
        owner_id=current_user.user_id,
    )


# preflight options req for /playlist
@playlist_router.options("", response_model=schemas.Playlist)
async def options_playlist():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, POST, PATCH, DELETE",
            "Access-Control-Allow-Headers": "accept, Authorization, Content-Type",
        }
    )


# add a track to a playlist for the current user
@playlist_router.patch(
    "/{playlist_id}/track/{track_id}",
    response_model=schemas.Playlist,
    status_code=201,
)
async def add_track_to_playlist(
    current_user: dependencies.current_user,
    playlist: dependencies.playlist,
    track: dependencies.track,
    db: dependencies.database,
):
    """
    The order of the dependencies is important. We first want to check if the user
    is logged in, then we check if the playlist exists and if the user owns it.

    This is so we can avoid a database call if the user is not logged in. Also stops
    someone inferring the existence of a playlist by checking if they get a 404 or 401.
    """
    # only allow a user to add a track to a playlist they own
    if playlist.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )
    return db.playlist.add_track_to_playlist(playlist, track)


# remove a track from a playlist for the current user
@playlist_router.delete(
    "/{playlist_id}/track/{track_id}",
    response_model=schemas.Playlist,
    status_code=201,
)
async def remove_track_from_playlist(
    current_user: dependencies.current_user,
    playlist: dependencies.playlist,
    track: dependencies.track,
    db: dependencies.database,
):
    if playlist.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )

    return db.playlist.remove_track_from_playlist(playlist, track)


# delete playlist for the current user
@playlist_router.delete(
    "/{playlist_id}",
    status_code=204,
)
async def delete_playlist(
    current_user: dependencies.current_user,
    playlist: dependencies.playlist,
    db: dependencies.database,
):
    if playlist.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )
    db.playlist.delete(playlist)
    return Response(status_code=204)


# options req for /playlist/{playlist_id}
@playlist_router.options("/{playlist_id}", response_model=schemas.Playlist)
async def options_playlist_id():
    return Response(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS, DELETE",
            "Access-Control-Allow-Headers": "accept, Authorization, Content-Type",
        }
    )


# update playlist name for the current user
@playlist_router.patch(
    "",
    response_model=schemas.Playlist,
    status_code=201,
)
async def update_playlist(updated_playlist: dependencies.updated_playlist):
    return updated_playlist
