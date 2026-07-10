#!/bin/bash
set -e
echo "LIGHT ONE V2 배포 시작..."
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
echo "배포 완료!"
