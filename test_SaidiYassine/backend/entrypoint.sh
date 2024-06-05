#!/bin/sh

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data.json


# Start server
python manage.py runserver 0.0.0.0:8000
