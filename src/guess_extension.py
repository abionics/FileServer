import mimetypes

import filetype
import magic


def guess_extension_by_content(content: bytes) -> str | None:
    return _by_filetype(content) or _by_magic(content)


def guess_extension_by_mime_type(mime_type: str) -> str | None:
    return _by_mime_type(mime_type)


def _by_filetype(content: bytes) -> str | None:
    kind = filetype.guess(content)
    if kind is not None:
        return kind.extension


def _by_magic(content: bytes) -> str | None:
    mime_type = magic.from_buffer(content, mime=True)
    return _by_mime_type(mime_type)


def _by_mime_type(mime_type: str) -> str | None:
    extension = mimetypes.guess_extension(mime_type, strict=False)
    if extension is not None:
        return extension.removeprefix('.')
