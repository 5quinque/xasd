import mutagen


def track_info(filepath):
    track_info = mutagen.File(filepath, easy=True)

    single_info = {
        "album": track_info.get("album", [None]).pop(),
        "title": track_info.get("title", [None]).pop(),
        "artist": track_info.get("artist", [None]).pop(),
        "tracknumber": track_info.get("tracknumber", [None]).pop(),
        "genre": track_info.get("genre", [None]).pop(),
        "date": track_info.get("date", [None]).pop(),
        "hash": None,
    }

    return single_info
