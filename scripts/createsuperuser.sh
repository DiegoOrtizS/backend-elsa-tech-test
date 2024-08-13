#!/bin/sh
DJANGO_SUPERUSER_USERNAME=admin@admin.com \
DJANGO_SUPERUSER_PASSWORD=testpass123 \
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
python manage.py createsuperuser --noinput --first_name=admin --last_name=admin
