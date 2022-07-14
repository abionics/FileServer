import os

from aiohttp import ClientTimeout

REQUEST_TIMEOUT = ClientTimeout(
    total=int(os.getenv('REQUEST_TIMEOUT', '30'))
)

FILE_FOLDER = os.getenv('FILE_FOLDER', 'files')

UNKNOWN_EXTENSION = os.getenv('FILE_FOLDER', 'unknown')
