2025-07-06T12:01:33.425164442Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 485, in check
2025-07-06T12:01:33.425168952Z     all_issues = checks.run_checks(
2025-07-06T12:01:33.425173543Z         app_configs=app_configs,
2025-07-06T12:01:33.425177773Z     ...<2 lines>...
2025-07-06T12:01:33.425181843Z         databases=databases,
2025-07-06T12:01:33.425185733Z     )
2025-07-06T12:01:33.425189914Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 88, in run_checks
2025-07-06T12:01:33.425194834Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-07-06T12:01:33.425198814Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 14, in check_url_config
2025-07-06T12:01:33.425202645Z     return check_resolver(resolver)
2025-07-06T12:01:33.425206825Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 24, in check_resolver
2025-07-06T12:01:33.425210885Z     return check_method()
2025-07-06T12:01:33.425215415Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 494, in check
2025-07-06T12:01:33.425219575Z     for pattern in self.url_patterns:
2025-07-06T12:01:33.425223246Z                    ^^^^^^^^^^^^^^^^^
2025-07-06T12:01:33.425227206Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:01:33.425242247Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:01:33.425244857Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:01:33.425247317Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 715, in url_patterns
2025-07-06T12:01:33.425249957Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-07-06T12:01:33.425252428Z                        ^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:33.425254898Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:01:33.425257508Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:01:33.425259888Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:01:33.425262598Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 708, in urlconf_module
2025-07-06T12:01:33.425265038Z     return import_module(self.urlconf_name)
2025-07-06T12:01:33.425267998Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:01:33.425270398Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:01:33.425272979Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:33.425275649Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:01:33.425278029Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:01:33.425280389Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:01:33.425282659Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:01:33.42528535Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:01:33.42528769Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:01:33.42528992Z   File "/opt/render/project/src/payroll/urls.py", line 38, in <module>
2025-07-06T12:01:33.42529249Z     path('admin/payroll/', include('employees.admin_urls', namespace='payroll_admin')),
2025-07-06T12:01:33.42530268Z                            ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:33.425305631Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 38, in include
2025-07-06T12:01:33.425308081Z     urlconf_module = import_module(urlconf_module)
2025-07-06T12:01:33.425310361Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:01:33.425312791Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:01:33.425315071Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:33.425317871Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:01:33.425320292Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:01:33.425322602Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:01:33.425324952Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:01:33.425327292Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:01:33.425329582Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:01:33.425331752Z   File "/opt/render/project/src/employees/admin_urls.py", line 2, in <module>
2025-07-06T12:01:33.425334192Z     from . import admin_views
2025-07-06T12:01:33.425338622Z   File "/opt/render/project/src/employees/admin_views.py", line 9, in <module>
2025-07-06T12:01:33.425345703Z     from .models import Organization, Department
2025-07-06T12:01:33.425348133Z   File "/opt/render/project/src/employees/models.py", line 6, in <module>
2025-07-06T12:01:33.425350513Z     class Organization(models.Model):
2025-07-06T12:01:33.425352963Z     ...<152 lines>...
2025-07-06T12:01:33.425355294Z             ordering = ['organization_type', 'name']
2025-07-06T12:01:33.425357644Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 134, in __new__
2025-07-06T12:01:33.425360304Z     raise RuntimeError(
2025-07-06T12:01:33.425362644Z     ...<3 lines>...
2025-07-06T12:01:33.425365314Z     )
2025-07-06T12:01:33.425368074Z RuntimeError: Model class employees.models.Organization doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
2025-07-06T12:01:34.750773037Z ==> Exited with status 1
2025-07-06T12:01:34.768679156Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
2025-07-06T12:01:43.070575621Z ==> Running 'python manage.py migrate && gunicorn payroll.wsgi:application'
2025-07-06T12:01:49.972949016Z Traceback (most recent call last):
2025-07-06T12:01:49.97759553Z   File "/opt/render/project/src/manage.py", line 22, in <module>
2025-07-06T12:01:49.97760772Z     main()
2025-07-06T12:01:49.97761172Z     ~~~~^^
2025-07-06T12:01:49.977615321Z   File "/opt/render/project/src/manage.py", line 18, in main
2025-07-06T12:01:49.977620881Z     execute_from_command_line(sys.argv)
2025-07-06T12:01:49.977624901Z     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-07-06T12:01:49.977639082Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2025-07-06T12:01:49.977645922Z     utility.execute()
2025-07-06T12:01:49.977649553Z     ~~~~~~~~~~~~~~~^^
2025-07-06T12:01:49.977653483Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 436, in execute
2025-07-06T12:01:49.977657033Z     self.fetch_command(subcommand).run_from_argv(self.argv)
2025-07-06T12:01:49.977660483Z     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-07-06T12:01:49.977664063Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 412, in run_from_argv
2025-07-06T12:01:49.977667544Z     self.execute(*args, **cmd_options)
2025-07-06T12:01:49.977671074Z     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977674464Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 458, in execute
2025-07-06T12:01:49.977677914Z     output = self.handle(*args, **options)
2025-07-06T12:01:49.977681215Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 106, in wrapper
2025-07-06T12:01:49.977684565Z     res = handle_func(*args, **kwargs)
2025-07-06T12:01:49.977687925Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/commands/migrate.py", line 100, in handle
2025-07-06T12:01:49.977691465Z     self.check(databases=[database])
2025-07-06T12:01:49.977694895Z     ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977698446Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 485, in check
2025-07-06T12:01:49.977702016Z     all_issues = checks.run_checks(
2025-07-06T12:01:49.977705576Z         app_configs=app_configs,
2025-07-06T12:01:49.977708886Z     ...<2 lines>...
2025-07-06T12:01:49.977712486Z         databases=databases,
2025-07-06T12:01:49.977715897Z     )
2025-07-06T12:01:49.977719327Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 88, in run_checks
2025-07-06T12:01:49.977722957Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-07-06T12:01:49.977726477Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 14, in check_url_config
2025-07-06T12:01:49.977729967Z     return check_resolver(resolver)
2025-07-06T12:01:49.977733438Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 24, in check_resolver
2025-07-06T12:01:49.977736798Z     return check_method()
2025-07-06T12:01:49.977740608Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 494, in check
2025-07-06T12:01:49.977743998Z     for pattern in self.url_patterns:
2025-07-06T12:01:49.977747419Z                    ^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977750829Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:01:49.977762599Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:01:49.9777649Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:01:49.97776709Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 715, in url_patterns
2025-07-06T12:01:49.97776921Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-07-06T12:01:49.97777136Z                        ^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.97777347Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:01:49.97777552Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:01:49.97777764Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:01:49.97777974Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 708, in urlconf_module
2025-07-06T12:01:49.97778181Z     return import_module(self.urlconf_name)
2025-07-06T12:01:49.977783991Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:01:49.977786021Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:01:49.977788251Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977790431Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:01:49.977792581Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:01:49.977794741Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:01:49.977796851Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:01:49.977799011Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:01:49.977801042Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:01:49.977803042Z   File "/opt/render/project/src/payroll/urls.py", line 38, in <module>
2025-07-06T12:01:49.977805152Z     path('admin/payroll/', include('employees.admin_urls', namespace='payroll_admin')),
2025-07-06T12:01:49.977809152Z                            ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977811492Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 38, in include
2025-07-06T12:01:49.977813602Z     urlconf_module = import_module(urlconf_module)
2025-07-06T12:01:49.977815623Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:01:49.977817673Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:01:49.977819803Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:01:49.977825513Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:01:49.977827853Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:01:49.977829913Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:01:49.977831964Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:01:49.977834033Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:01:49.977836104Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:01:49.977838034Z   File "/opt/render/project/src/employees/admin_urls.py", line 2, in <module>
2025-07-06T12:01:49.977840174Z     from . import admin_views
2025-07-06T12:01:49.977842294Z   File "/opt/render/project/src/employees/admin_views.py", line 9, in <module>
2025-07-06T12:01:49.977848314Z     from .models import Organization, Department
2025-07-06T12:01:49.977850574Z   File "/opt/render/project/src/employees/models.py", line 6, in <module>
2025-07-06T12:01:49.977852735Z     class Organization(models.Model):
2025-07-06T12:01:49.977854825Z     ...<152 lines>...
2025-07-06T12:01:49.977856915Z             ordering = ['organization_type', 'name']
2025-07-06T12:01:49.977858985Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 134, in __new__
2025-07-06T12:01:49.977861195Z     raise RuntimeError(
2025-07-06T12:01:49.977863255Z     ...<3 lines>...
2025-07-06T12:01:49.977865265Z     )
2025-07-06T12:01:49.977867375Z RuntimeError: Model class employees.models.Organization doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.