release: python manage.py migrate
web: gunicorn config.wsgi:application --max-requests 1000


