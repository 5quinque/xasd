from mite.scenario import StopVolumeModel

from datapools import artists, random_strings, track_ids


def volume_model_factory(n, duration=60 * 15):
    def vm(start, end):
        if start > duration:
            raise StopVolumeModel
        return n

    vm.__name__ = f"volume model {n}"
    return vm


scenarios = [
    (10, "journeys:read_tracks_journey", None),
    (10, "journeys:read_track_journey", track_ids),
    (10, "journeys:read_file_journey", track_ids),
    (10, "journeys:read_albums_by_artist_journey", artists),
    (10, "journeys:read_tracks_by_artist_journey", artists),
    (10, "journeys:search_any_journey", random_strings),
    (10, "journeys:search_track_journey", random_strings),
    (2, "journeys:health_journey", None),
]


# Peak scenario running at full TPS for 1 hour
def peak_scenario():
    for peak, journey, datapool in scenarios:
        yield journey, datapool, volume_model_factory(peak, duration=1 * 60 * 60)


# Soak scenario running at a third TPS for 6 hours
def soak_scenario():
    for peak, journey, datapool in scenarios:
        yield journey, datapool, volume_model_factory(peak / 3, duration=6 * 60 * 60)


# Quick scenario running at full TPS for default time of 5 minute
def quick_scenario():
    for peak, journey, datapool in scenarios:
        yield journey, datapool, volume_model_factory(peak)
