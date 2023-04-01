from mite_http import mite_http
from mite import ensure_fixed_separation

from api import XasdAPI

from mite_http import mite_http


@mite_http
async def read_tracks_journey(ctx):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.read_tracks()


@mite_http
async def read_track_journey(ctx, track_id):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.read_track(track_id)


@mite_http
async def read_test(ctx):
    async with ensure_fixed_separation(1):
        return await ctx.http.get(f"http://172.17.0.1:8000/test")


@mite_http
async def read_file_journey(ctx, track_id):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.read_file(track_id)


@mite_http
async def read_albums_by_artist_journey(ctx, artist_name):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.read_albums_by_artist(artist_name)


@mite_http
async def read_tracks_by_artist_journey(ctx, artist_name):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.read_tracks_by_artist(artist_name)


@mite_http
async def search_any_journey(ctx, query):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.search_any(query)


@mite_http
async def search_track_journey(ctx, query):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.search_track(query)


@mite_http
async def health_journey(ctx):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.health()
