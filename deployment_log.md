2025-07-06T12:21:57.634386268Z     execute_from_command_line(sys.argv)
2025-07-06T12:21:57.634390488Z     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-07-06T12:21:57.634396149Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2025-07-06T12:21:57.634401298Z     utility.execute()
2025-07-06T12:21:57.634405289Z     ~~~~~~~~~~~~~~~^^
2025-07-06T12:21:57.634410359Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 436, in execute
2025-07-06T12:21:57.634414769Z     self.fetch_command(subcommand).run_from_argv(self.argv)
2025-07-06T12:21:57.634419239Z     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-07-06T12:21:57.634423329Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 412, in run_from_argv
2025-07-06T12:21:57.634427739Z     self.execute(*args, **cmd_options)
2025-07-06T12:21:57.634432429Z     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:21:57.634436889Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 458, in execute
2025-07-06T12:21:57.634441429Z     output = self.handle(*args, **options)
2025-07-06T12:21:57.634445749Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/commands/shell.py", line 117, in handle
2025-07-06T12:21:57.63446462Z     exec(options["command"], globals())
2025-07-06T12:21:57.63446743Z     ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:21:57.63448477Z   File "<string>", line 1
2025-07-06T12:21:57.63448892Z     from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'tidings@outlook.com', '@Admin2025') 
2025-07-06T12:21:57.63449216Z IndentationError: unexpected indent
2025-07-06T12:22:01.104359828Z ==> Exited with status 1
2025-07-06T12:22:01.122435207Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
2025-07-06T12:22:08.045833294Z ==> Running 'python manage.py migrate && python manage.py shell -c " from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'tidings@outlook.com', '@Admin2025') " && gunicorn payroll.wsgi:application'
2025-07-06T12:22:15.741252139Z Operations to perform:
2025-07-06T12:22:15.741287009Z   Apply all migrations: admin, auth, contenttypes, sessions
2025-07-06T12:22:15.741292109Z Running migrations:
2025-07-06T12:22:15.741296369Z   No migrations to apply.
2025-07-06T12:22:18.741215842Z Traceback (most recent call last):
2025-07-06T12:22:18.742277892Z   File "/opt/render/project/src/manage.py", line 22, in <module>
2025-07-06T12:22:18.742289272Z     main()
2025-07-06T12:22:18.742293242Z     ~~~~^^
2025-07-06T12:22:18.742297052Z   File "/opt/render/project/src/manage.py", line 18, in main
2025-07-06T12:22:18.742301162Z     execute_from_command_line(sys.argv)
2025-07-06T12:22:18.742305013Z     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-07-06T12:22:18.742309233Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2025-07-06T12:22:18.742313443Z     utility.execute()
2025-07-06T12:22:18.742317603Z     ~~~~~~~~~~~~~~~^^
2025-07-06T12:22:18.742322323Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 436, in execute
2025-07-06T12:22:18.742326413Z     self.fetch_command(subcommand).run_from_argv(self.argv)
2025-07-06T12:22:18.742330313Z     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-07-06T12:22:18.742334223Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 412, in run_from_argv
2025-07-06T12:22:18.742338083Z     self.execute(*args, **cmd_options)
2025-07-06T12:22:18.742341813Z     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:22:18.742345613Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 458, in execute
2025-07-06T12:22:18.742349603Z     output = self.handle(*args, **options)
2025-07-06T12:22:18.74378159Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/commands/shell.py", line 117, in handle
2025-07-06T12:22:18.743799041Z     exec(options["command"], globals())
2025-07-06T12:22:18.743803231Z     ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:22:18.743821891Z   File "<string>", line 1
2025-07-06T12:22:18.743829201Z     from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'tidings@outlook.com', '@Admin2025') 
2025-07-06T12:22:18.743833321Z IndentationError: unexpected indent