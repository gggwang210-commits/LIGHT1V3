"""Backward-compatible local wrapper for the guarded seed command."""

import os

import django
from django.core.management import call_command


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings_local')
django.setup()


if __name__ == '__main__':
    print('setup_dummy.py is deprecated; delegating to seed_lightone.')
    call_command('seed_lightone', '--generate-passwords')
