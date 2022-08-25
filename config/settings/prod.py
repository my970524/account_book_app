import os

from .base import *  # noqa
from .my_settings import DATABASES

DEBUG = False

ALLOWED_HOSTS = ["13.124.201.55", "django"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

DATABASES = DATABASES
