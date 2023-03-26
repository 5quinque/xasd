class XasdAPI:
    def __init__(self, ctx):
        self.ctx = ctx
        self._base_url = "http://172.17.0.1:8000"

    async def health(self):
        async with self.ctx.transaction("url1"):
            return await self.ctx.http.get(f"{self._base_url}/health")
