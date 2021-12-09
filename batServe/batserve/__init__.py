from .batserve import get_args, batserve

from gevent import monkey

monkey.patch_all()

import os
import sys
import glob
import time
import uuid
import falcon
import gevent
import shutil
import psutil
import socket
import logging
import mimetypes
import gunicorn.app.base
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO, format="%(message)s", handlers=[RichHandler(markup=True)]
)

batserve()
