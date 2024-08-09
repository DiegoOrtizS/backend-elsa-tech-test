#!/bin/sh
python manage.py make migrations
python manage.py migrate