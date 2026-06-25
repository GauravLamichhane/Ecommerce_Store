import os
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [host for host in os.environ.get('ALLOWED_HOSTS', '').split(',') if host]