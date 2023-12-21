import asyncio
from urllib.parse import urljoin

import aiohttp
from aiohttp import FormData

BUCKET = 'test'
BASE_URL = f'http://localhost:8000/{BUCKET}/'
FILEPATH_1 = 'scripts/test_upload.py'
SAVE_FILEPATH_1 = 'directory/test_upload.py'
FILEPATH_2 = 'scripts/main_dev.py'
SAVE_FILEPATH_2 = 'directory/main_dev.py'


async def upload_file(filename: str = '', content_type: str | None = None):
    data = FormData()
    data.add_field('file', _read_file(FILEPATH_1), filename=filename, content_type=content_type)
    url = urljoin(BASE_URL, 'upload/file')
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            print(await response.text())


async def upload_files():
    data = FormData()
    data.add_field('files', _read_file(FILEPATH_1), filename=SAVE_FILEPATH_1)
    data.add_field('files', _read_file(FILEPATH_2), filename=SAVE_FILEPATH_2)
    url = urljoin(BASE_URL, 'upload/files')
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            print(await response.text())


def _read_file(filepath: str) -> bytes:
    with open(filepath, 'rb') as file:
        return file.read()


async def main():
    await upload_file()
    await upload_file(
        filename=SAVE_FILEPATH_1,
        content_type='text/plain',
    )
    await upload_files()


if __name__ == '__main__':
    asyncio.run(main())
