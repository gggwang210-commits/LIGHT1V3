"""Fail-closed production settings for a separately managed deployment."""

from decouple import UndefinedValueError, config
from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F403,F401


def required(name):
    try:
        value = config(name)
    except UndefinedValueError as exc:
        raise ImproperlyConfigured(f'{name} is required in production.') from exc
    if not value.strip():
        raise ImproperlyConfigured(f'{name} must not be empty in production.')
    return value


if DEBUG:  # noqa: F405
    raise ImproperlyConfigured('DEBUG must be False in production.')
if not ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured('ALLOWED_HOSTS is required in production.')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': required('POSTGRES_DB'),
        'USER': required('POSTGRES_USER'),
        'PASSWORD': required('POSTGRES_PASSWORD'),
        'HOST': required('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': config('POSTGRES_CONN_MAX_AGE', default=60, cast=int),
        'OPTIONS': {'sslmode': config('POSTGRES_SSLMODE', default='require')},
    }
}

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    'SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool
)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
