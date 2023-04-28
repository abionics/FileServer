import hashlib

from pydantic import BaseModel

from utils import guess_extension_by_content


class FileData:

    def __init__(self, content: bytes, extension: str | None):
        self.content = content
        self.extension = self._detect_extension(content, extension)

    @staticmethod
    def _detect_extension(content: bytes, extension: str | None) -> str:
        if extension is not None:
            extension = extension.strip()
            if extension != '':
                return extension
        return guess_extension_by_content(content)

    def hash(self) -> str:
        return hashlib.md5(self.content).hexdigest()

    def filename(self) -> str:
        name = self.hash()
        return f'{name}.{self.extension}' if self.extension else name


class Query(BaseModel):
    url: str
    method: str = 'GET'
    data: dict = None
