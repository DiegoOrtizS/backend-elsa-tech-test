#!/bin/sh
DJANGO_SUPERUSER_USERNAME=admin@admin.com \
DJANGO_SUPERUSER_PASSWORD=testpass \
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
python manage.py createsuperuser --noinput
