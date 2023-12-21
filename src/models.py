import os

from pydantic import BaseModel

from config import STORAGE_DIRECTORY


class Blob(BaseModel):
    bucket: str
    content: bytes
    path: str

    @property
    def size(self) -> int:
        return len(self.content)

    def create_filepath(self) -> str:
        filepath = os.path.join(STORAGE_DIRECTORY, self.bucket, self.path)
        return os.path.abspath(filepath)


class Query(BaseModel):
    url: str
    method: str = 'GET'
    data: dict | None = None
    save_path: str | None = None
