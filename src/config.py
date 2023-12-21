import os

from aiohttp import ClientTimeout

STORAGE_DIRECTORY = os.path.abspath(
    os.getenv('STORAGE_DIRECTORY', 'files')
)

REQUEST_TIMEOUT = ClientTimeout(
    total=int(os.getenv('REQUEST_TIMEOUT_TOTAL', '30'))
)

DEFAULT_EXTENSION = os.getenv('DEFAULT_EXTENSION', 'bin')
