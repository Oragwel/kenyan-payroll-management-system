web: gunicorn payroll.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60
release: python manage.py migrate && python manage.py create_production_superuser
