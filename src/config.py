import os
import sys

from aiohttp import ClientTimeout
from loguru import logger

STORAGE_DIRECTORY = os.path.abspath(
    os.getenv('STORAGE_DIRECTORY', 'files')
)
REQUEST_TIMEOUT = ClientTimeout(
    total=int(os.getenv('REQUEST_TIMEOUT_TOTAL', '30'))
)
DEFAULT_EXTENSION = os.getenv('DEFAULT_EXTENSION', 'bin')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)
