import asyncio.exceptions
from typing import Callable

from aiohttp import ClientError
from fastapi import FastAPI, UploadFile, Body
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from loguru import logger

from exception import FileServerException
from models import Query
from storage import parse_file, request_file, parse_base64, save


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


@app.post('/{bucket}/upload/files')
async def upload_file(bucket: str, files: list[UploadFile]) -> list[dict]:
    return await asyncio.gather(*(
        _upload_file(bucket, file)
        for file in files
    ))


@app.post('/{bucket}/upload/file')
async def upload_file(bucket: str, file: UploadFile) -> dict:
    return await _upload_file(bucket, file)


@app.post('/{bucket}/upload/url')
async def upload_url(bucket: str, query: Query) -> dict:
    blob = await request_file(bucket, query)
    return await save(blob)


@app.post('/{bucket}/upload/base64')
async def upload_base64(bucket: str, content: str = Body(), path: str = Body(None)) -> dict:
    blob = await parse_base64(bucket, content, path)
    return await save(blob)


async def _upload_file(bucket: str, file: UploadFile) -> dict:
    blob = await parse_file(bucket, file)
    return await save(blob)
