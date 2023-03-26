from mite_http import mite_http
from mite import ensure_fixed_separation

from api import XasdAPI

from mite_http import mite_http


@mite_http
async def health_journey(ctx):
    xasdAPI = XasdAPI(ctx)
    async with ensure_fixed_separation(1):
        await xasdAPI.health()
