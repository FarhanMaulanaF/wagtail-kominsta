from .base import *

DEBUG = False

ALLOWED_HOSTS = ['farhanmaulanafirmansyah.pythonanywhere.com']

ROOT_URLCONF = "kominsta.urls"

SECRET_KEY = "2b_938l%h4*h*r&=xqa_r4zus9spj8m-vq$j=qwk^2kq5irzb9"

try:
    from .local import *
except ImportError:
    pass
