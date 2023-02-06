from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "2b_938l%h4*h*r&=xqa_r4zus9spj8m-vq$j=qwk^2kq5irzb9"

try:
    from .local import *
except ImportError:
    pass
