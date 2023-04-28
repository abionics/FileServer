import asyncio

import aiohttp
from aiohttp import FormData

URL = 'http://localhost:8000/test/upload/file'
FILENAME = 'upload_file_test.py'


async def upload_file():
    content = read_file()
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data={'file': content}) as response:
            print(await response.text())


async def upload_file_with_name():
    data = FormData()
    data.add_field('file', read_file(), filename=FILENAME, content_type='text/plain')
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data=data) as response:
            print(await response.text())


def read_file() -> bytes:
    with open(FILENAME, 'rb') as file:
        return file.read()


if __name__ == '__main__':
    asyncio.run(upload_file())
    asyncio.run(upload_file_with_name())
