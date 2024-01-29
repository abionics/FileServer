import asyncio
import base64
import os
from urllib.parse import unquote

from aiohttp import ClientSession, ClientResponse
from farmhash import FarmHash128
from fastapi import UploadFile
from loguru import logger

from config import STORAGE_DIRECTORY, REQUEST_TIMEOUT, DEFAULT_EXTENSION
from exception import FileServerException
from guess_extension import guess_extension_by_content, guess_extension_by_mime_type
from models import Blob, Query


async def parse_file(bucket: str, file: UploadFile) -> Blob:
    content = await file.read()
    path = _create_path(content, file.filename)
    return Blob(bucket=bucket, content=content, path=path)


async def request_file(bucket: str, query: Query) -> Blob:
    async with ClientSession(timeout=REQUEST_TIMEOUT) as session:
        async with session.request(query.method, query.url, data=query.data, verify_ssl=False) as response:
            if not 200 <= response.status < 300:
                raise FileServerException(f'Error response code {response.status}')
            content = await response.content.read()
    extension = _response_to_extension(response)
    path = _create_path(content, query.save_path, extension)
    return Blob(bucket=bucket, content=content, path=path)


async def parse_base64(bucket: str, content: str, path: str | None) -> Blob:
    content = base64.b64decode(content)
    path = _create_path(content, path)
    return Blob(bucket=bucket, content=content, path=path)


def _create_path(content: bytes, path: str | None, extension: str | None = None) -> str:
    if path:
        return unquote(path).strip()
    filename = FarmHash128(content)
    if extension is None:
        extension = guess_extension_by_content(content) or DEFAULT_EXTENSION
    return f'{filename:x}.{extension}'


def _response_to_extension(response: ClientResponse) -> str | None:
    if 'content-type' not in response.headers:
        return None
    content_type = response.headers['content-type'].strip(';/\n\t')
    mime_type = content_type.split(';')[0]
    return guess_extension_by_mime_type(mime_type)


async def save(blob: Blob) -> dict:
    return await asyncio.to_thread(save_sync, blob)


def save_sync(blob: Blob) -> dict:
    filepath = blob.create_filepath()
    check_filepath(filepath)
    if os.path.exists(filepath):
        logger.debug(f'File "{blob.path}" is already exist in bucket "{blob.bucket}"')
        return {'path': blob.path, 'exists': True}
    directory = os.path.dirname(filepath)
    os.makedirs(directory, exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(blob.content)
    logger.debug(f'Saved "{blob.path}" in bucket "{blob.bucket}", size is {blob.size} bytes')
    return {'path': blob.path, 'exists': False}


def check_filepath(filepath: str):
    if not filepath.startswith(STORAGE_DIRECTORY):
        raise FileServerException(f'Invalid path "{filepath}"')


def check_access(bucket: str, mkdir: bool) -> bool:
    path = os.path.join(STORAGE_DIRECTORY, bucket)
    if mkdir:
        os.makedirs(path, exist_ok=True)
    return os.access(path, os.R_OK | os.W_OK)
