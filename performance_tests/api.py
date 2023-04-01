class XasdAPI:
    def __init__(self, ctx):
        self.ctx = ctx
        self._base_url = "http://172.17.0.1:8000"

    async def read_tracks(self):
        async with self.ctx.transaction("XASD Read Tracks"):
            return await self.ctx.http.get(f"{self._base_url}/track")

    async def read_track(self, track_id):
        async with self.ctx.transaction("XASD Read Track"):
            return await self.ctx.http.get(f"{self._base_url}/track/{track_id}")

    async def read_file(self, track_id):
        async with self.ctx.transaction("XASD Read File"):
            return await self.ctx.http.get(f"{self._base_url}/track/{track_id}/file")

    async def read_albums_by_artist(self, arist_name):
        async with self.ctx.transaction("XASD Read Albums"):
            return await self.ctx.http.get(
                f"{self._base_url}/artist/{arist_name}/albums"
            )

    async def read_tracks_by_artist(self, arist_name):
        async with self.ctx.transaction("XASD Read Tracks"):
            return await self.ctx.http.get(
                f"{self._base_url}/artist/{arist_name}/tracks"
            )

    async def search_any(self, query):
        async with self.ctx.transaction("XASD Search Any"):
            return await self.ctx.http.get(f"{self._base_url}/search/any/{query}")

    async def search_track(self, query):
        async with self.ctx.transaction("XASD Search Track"):
            return await self.ctx.http.get(f"{self._base_url}/search/track/{query}")

    async def health(self):
        async with self.ctx.transaction("XASD Health Check"):
            return await self.ctx.http.get(f"{self._base_url}/health")
