import os

from aiohttp import ClientTimeout

REQUEST_TIMEOUT_TOTAL = int(os.getenv('REQUEST_TIMEOUT_TOTAL', '30'))
REQUEST_TIMEOUT = ClientTimeout(
    total=REQUEST_TIMEOUT_TOTAL
)

FILE_FOLDER = os.getenv('FILE_FOLDER', 'files')
