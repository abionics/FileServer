import asyncio.exceptions
import base64
import os
from typing import Callable

import aiohttp
from aiohttp import ClientError
from fastapi import FastAPI, UploadFile, Body
from fastapi.requests import Request
from loguru import logger
from starlette.responses import Response, JSONResponse

from config import REQUEST_TIMEOUT, FILE_FOLDER
from exception import FileServerException
from models import FileData, Query
from utils import guess_extension_by_mime_type


async def catch_exceptions_middleware(request: Request, endpoint: Callable) -> Response:
    try:
        return await endpoint(request)
    except asyncio.exceptions.TimeoutError:
        e = 'Request timeout'
        logger.warning(e)
        return JSONResponse(status_code=400, content={'exception': str(e)})
    except (FileServerException, ClientError) as e:
        logger.warning(e)
        return JSONResponse(status_code=400, content={'exception': str(e)})
    except BaseException as e:
        logger.exception(e)
        return Response(status_code=500, content='Internal server error')


app = FastAPI()
app.middleware('http')(catch_exceptions_middleware)


@app.post('/{bucket}/upload/file')
async def upload_file(bucket: str, file: UploadFile) -> dict:
    data = await _parse_file(file)
    return await _save(bucket, data)


@app.post('/{bucket}/upload/url')
async def upload_url(bucket: str, query: Query) -> dict:
    data = await _request_file(query)
    return await _save(bucket, data)


@app.post('/{bucket}/upload/base64')
async def upload_base64(bucket: str, content: str = Body(), extension: str = Body(default=None)) -> dict:
    content = base64.b64decode(content)
    data = FileData(content, extension)
    return await _save(bucket, data)


async def _parse_file(file: UploadFile) -> FileData:
    content = await file.read()
    extension = file.filename.split('.')[-1]
    return FileData(content, extension)


async def _request_file(query: Query) -> FileData:
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        async with session.request(query.method, query.url, data=query.data, verify_ssl=False) as response:
            if not 200 <= response.status < 300:
                raise FileServerException(f'Error response code {response.status}')
            content = await response.content.read()
            content_type = response.headers.get('content-type', '').strip(';/\n\t')
            mime_type = content_type.split(';')[0]
            extension = guess_extension_by_mime_type(mime_type)
            return FileData(content, extension)


async def _save(bucket: str, data: FileData) -> dict:
    filename = data.filename()
    directory = os.path.join(FILE_FOLDER, bucket)
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        logger.warning(f'File "{filename}" is already exist in bucket "{bucket}"')
    else:
        os.makedirs(directory, exist_ok=True)
        with open(path, 'wb') as file:
            file.write(data.content)
        size = len(data.content)
        logger.success(f'Saved "{filename}" in bucket "{bucket}", size is {size} bytes')
    return {'filename': filename}
