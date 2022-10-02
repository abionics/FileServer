import mimetypes

import magic


def detect_extension(content: bytes) -> str:
    mime = magic.from_buffer(content, mime=True)
    return mime_to_extension(mime)


def mime_to_extension(mime: str) -> str:
    extension = mimetypes.guess_extension(mime)
    if extension is None:
        mime = mime.split(';')[0]
        extension = mimetypes.guess_extension(mime)
        if extension is None:
            return ''
    return extension.removeprefix('.')
