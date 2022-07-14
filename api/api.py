import base64
import hashlib
import os

import aiohttp
from fastapi import FastAPI, UploadFile, Body
from loguru import logger

from config import REQUEST_TIMEOUT, FILE_FOLDER
from models import FileData, Query
from utils import mime_to_extensions

app = FastAPI()


@app.post('/upload/file')
async def upload_file(file: UploadFile) -> dict:
    data = await _parse_file(file)
    return await _save(data)


@app.post('/upload/url')
async def upload_url(query: Query) -> dict:
    data = await _request_file(query)
    return await _save(data)


@app.post('/upload/base64')
async def upload_base64(content: str = Body(), extension: str = Body(default=None)) -> dict:
    content = base64.b64decode(content)
    data = FileData(content, extension)
    return await _save(data)


async def _parse_file(file: UploadFile) -> FileData:
    content = await file.read()
    extension = file.filename.split('.')[-1]
    return FileData(content, extension)


async def _request_file(query: Query) -> FileData:
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        async with session.request(query.method, query.url, data=query.data, verify_ssl=False) as response:
            if not 200 <= response.status < 300:
                raise Exception(f'Error response code {response.status} for {query=}')
            content = await response.content.read()
            content_type = response.headers.get('content-type', '').strip('/\n\t')
            extension = mime_to_extensions(content_type)
            return FileData(content, extension)


async def _save(data: FileData) -> dict:
    md5 = hashlib.md5(data.content).hexdigest()
    filename = f'{md5}.{data.extension}'
    filepath = os.path.join(FILE_FOLDER, filename)
    if os.path.exists(filepath):
        logger.warning(f'File "{filename}" is already exist')
    else:
        length = len(data.content)
        with open(filepath, 'wb') as file:
            file.write(data.content)
        logger.success(f'Saved "{filename}", size is {length} bytes')
    return {'filename': filename}
