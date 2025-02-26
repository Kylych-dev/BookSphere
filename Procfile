web: gunicorn backend/core.wsgi --log-file -
web: python backend/manage.py migrate && gunicorn backend/core.wsgi