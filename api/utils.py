import mimetypes

import magic

from config import UNKNOWN_EXTENSION


def detect_extensions(content: bytes) -> str:
    mime = magic.from_buffer(content, mime=True)
    return mime_to_extensions(mime)


def mime_to_extensions(mime: str) -> str:
    return mimetypes.guess_extension(mime).removeprefix('.') or UNKNOWN_EXTENSION
