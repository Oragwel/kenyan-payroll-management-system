web: gunicorn payroll.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
release: python manage.py migrate && python create_superuser.py
