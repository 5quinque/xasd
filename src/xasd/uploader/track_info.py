import re
from typing import Dict, List, Optional

import mutagen


def track_info(filepath: str) -> Dict[str, Optional[str]]:
    """
    Extracts basic track information from an audio file and returns it as a dictionary.

    Args:
        filepath: A string representing the path to an audio file.

    Returns:
        A dictionary containing the following keys and values:
            - "album": A string representing the album name.
            - "title": A string representing the track title.
            - "artist": A string representing the artist name.
            - "tracknumber": A string representing the track number.
            - "genre": A string representing the genre.
            - "date": A string representing the release date.
            - "hash": None (not used).

            If any of the above tags are missing, their corresponding value will be None.

    Raises:
        TypeError: If filepath is not a string.
        ValueError: If the specified file cannot be read or is not a valid audio file.

    Examples:
        >>> track_info("my_song.mp3")
        {'album': 'My Album', 'title': 'My Song', 'artist': 'My Artist', 'tracknumber': '1', 'genre': 'Pop', 'date': '2022', 'hash': None}

        >>> track_info("nonexistent_file.mp3")
        Traceback (most recent call last):
            ...
        ValueError: Unable to read file nonexistent_file.mp3

        >>> track_info("invalid_file.txt")
        Traceback (most recent call last):
            ...
        ValueError: File invalid_file.txt is not a valid audio file
    """

    if not isinstance(filepath, str):
        raise TypeError("filepath must be a string")

    try:
        track_info = mutagen.File(filepath, easy=True)
    except IOError:
        raise ValueError(f"Unable to read file {filepath}")
    except mutagen.MutagenError:
        raise ValueError(f"File {filepath} is not a valid audio file")

    # The artist tag sometimes contains multiple artist, or features.
    # For now, just get the first artist
    i3d_artist = track_info.get("artist", [None]).pop()
    artist = artist_names(i3d_artist)[0] if i3d_artist else None

    return {
        "album": track_info.get("album", [None]).pop(),
        "title": track_info.get("title", [None]).pop(),
        "artist": artist,
        "tracknumber": track_info.get("tracknumber", [None]).pop(),
        "genre": track_info.get("genre", [None]).pop(),
        "date": track_info.get("date", [None]).pop(),
        "hash": None,
    }


def artist_names(artist_tag: str) -> List[str]:
    """
    Parses an i3d artist tag and returns a list of all the artist names.

    Args:
        artist_tag (str): A string representing an i3d artist tag, which may contain one or more artist names, separated by commas,
            "and", "&", "feat.", or "ft.".

    Returns:
        A list of strings, where each string represents an artist name.

    Raises:
        TypeError: If i3d_tag is not a string.

    Examples:
        >>> get_artist_names("Kendrick Lamar, Blxst, Amanda Reifer")
        ['Kendrick Lamar', 'Blxst', 'Amanda Reifer']

        >>> get_artist_names("Ariana Grande & The Weeknd")
        ['Ariana Grande', 'The Weeknd']

        >>> get_artist_names("Lil Nas X (feat. Billy Ray Cyrus)")
        ['Lil Nas X', 'Billy Ray Cyrus']
    """

    if not isinstance(artist_tag, str):
        raise TypeError("artist_tag must be a string")

    # Replace "&" with "," for consistency
    artist_tag = artist_tag.replace("&", ",")

    # Replace "/" with "," for consistency
    artist_tag = artist_tag.replace("/", ",")

    # Use regular expression to split on any separator, including "feat." or "ft."
    artists = re.split(r",|\s(?:feat\.?|ft\.)\s", artist_tag)

    # Remove leading/trailing whitespace and parentheses
    artists = [re.sub(r"^\s+|\s+$|\(|\)", "", artist) for artist in artists]

    return artists
