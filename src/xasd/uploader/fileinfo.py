import mimetypes

from uuid import uuid4


def mimetype(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)

    return mime_type


def generate_uuid_filename():
    random_uuid = uuid4()
    split_uuid = str(random_uuid).split("-")
    directory = split_uuid[0][:2]
    filename = "".join(split_uuid[1:])

    return f"{directory}/{filename}"
