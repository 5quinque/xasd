import random
import string

from mite.datapools import RecyclableIterableDataPool


def randomString(stringLength=5):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


track_ids = RecyclableIterableDataPool([(i,) for i in range(1, 500)])

artists = RecyclableIterableDataPool(
    [
        ("artist_name",),
    ]
    * 500
)

random_strings = RecyclableIterableDataPool([(randomString(3),) for _ in range(500)])
