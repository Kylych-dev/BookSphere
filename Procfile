web: gunicorn backend.core.wsgi --log-file -
#or works good with external database
web: python backend.manage.py migrate && gunicorn backend.core.wsgi