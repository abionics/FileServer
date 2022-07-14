from pydantic import BaseModel

from utils import detect_extensions


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
        return detect_extensions(content)


class Query(BaseModel):
    url: str
    method: str = 'GET'
    data: dict = None
