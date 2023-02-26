import mimetypes

from uuid import uuid4


def mimetype(filepath: str) -> str:
    """
    Returns the mimetype of a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The mimetype of the file.
    """
    mime_type, _ = mimetypes.guess_type(filepath)

    return mime_type


def generate_uuid_filename() -> str:
    """
    Generates a random UUID and returns a string of the first two characters
    of the first part of the UUID and the rest of the UUID.

    Returns:
        str: The generated UUID filename.
    """
    random_uuid = uuid4()
    split_uuid = str(random_uuid).split("-")
    directory = split_uuid[0][:2]
    filename = "".join(split_uuid[1:])

    return f"{directory}/{filename}"
