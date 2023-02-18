import tempfile

from PIL import Image
from pydub import AudioSegment
import imagehash
from typing import Union, Type

from xasd.database.crud import XasdDB
from xasd.database.models import Hash
from xasd.utils.constants import SUPPORTED_MIMETYPES


def file_hash(database: XasdDB, filepath: str, mimetype: str) -> Union[bool, Hash]:
    """
    Given a database, filepath and mimetype, this function generates a waveform and a perceptual hash of the image.
    It then adds the hash to the database, and returns a boolean indicating if the hash already exists in the database.

    Parameters:
    - database (XasdDB): The database object where the hash will be stored.
    - filepath (str): The path to the audio file.
    - mimetype (str): The mimetype of the image file.

    Returns:
    - bool or Hash: A boolean indicating if the hash already exists in the database, or the new hash if it's unique.
    """
    with tempfile.NamedTemporaryFile() as waveformimage:
        # Create a waveform
        create_waveform(filepath, mimetype, waveformimage.name)

        # Create a perceptual hash of the image
        hash = image_hash(waveformimage.name)

    # Search for the hash in the DB, will return false if the hash already exists
    return database.add_unique_hash(hash)


def _calculate_peaks(audio_file: bytes):
    """Returns a list of audio level peaks"""

    bar_count = 107
    db_ceiling = 60

    chunk_length = len(audio_file) / bar_count

    loudness_of_chunks = [
        audio_file[i * chunk_length : (i + 1) * chunk_length].rms
        for i in range(bar_count)
    ]

    max_rms = max(loudness_of_chunks) * 1.00

    return [int((loudness / max_rms) * db_ceiling) for loudness in loudness_of_chunks]


def _get_bar_image(size, fill):
    """Returns an image of a bar."""
    width, height = size
    bar = Image.new("RGBA", size, fill)

    end = Image.new("RGBA", (width, 2), fill)

    bar.paste(end, (0, 0))
    bar.paste(end.rotate(180), (0, height - 2))
    return bar


def create_waveform(audio_file: str, audio_mimetype: str, image_file: str) -> None:
    """
    Given an audio file, its mimetype, and an output image file, this function generates a waveform image of the audio.
    n.b. we don't currently upload this waveform anywhere. do we want to?

    Parameters:
    - audio_file (str): The path to the audio file.
    - audio_mimetype (str): The mimetype of the audio file.
    - image_file (str): The path to the output image file.

    Raises:
    - Exception: If the mimetype of the audio file is not recognised.
    """
    samples = audio_samples(audio_file, audio_mimetype)

    if samples is False:
        raise Exception("Not a recognised audio file")

    peaks = _calculate_peaks(samples)

    # Create a new image (840w x 128h), with a white bg
    im = Image.new("RGB", (840, 128), "#ffffff")

    for index, value in enumerate(peaks, start=0):
        column = index * 8 + 2
        upper_endpoint = 64 - value

        # Get the bar, fill it black
        im.paste(_get_bar_image((4, value * 2), "#000000"), (column, upper_endpoint))

    with open(image_file, "wb") as imfile:
        im.save(imfile, "PNG")


def audio_samples(audio_file: str, mimetype: str) -> Union[Type[AudioSegment], bool]:
    """
    Given an audio file and its mimetype, this function returns the audio samples as an AudioSegment object,
    if the mimetype is one of the supported formats.

    Parameters:
    - audio_file (str): The path to the audio file.
    - mimetype (str): The mimetype of the audio file.

    Returns:
    - AudioSegment or False: The audio samples as an AudioSegment object, or False if the mimetype is not supported.
    """
    if mimetype in SUPPORTED_MIMETYPES:
        sound = AudioSegment.from_file(audio_file)
        return sound

    return False


def image_hash(filepath: str) -> str:
    """
    Given a filepath, this function reads the image and returns its perceptual hash.

    Parameters:
    - filepath (str): The path to the image file.

    Returns:
    - str: The perceptual hash of the image as a string.
    """
    image = Image.open(filepath)

    return imagehash.phash(image, hash_size=8)
