2025-07-06T12:55:05.076140685Z     ...<2 lines>...
2025-07-06T12:55:05.076143485Z         databases=databases,
2025-07-06T12:55:05.076146115Z     )
2025-07-06T12:55:05.076148905Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 88, in run_checks
2025-07-06T12:55:05.076153905Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-07-06T12:55:05.076156565Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 42, in check_url_namespaces_unique
2025-07-06T12:55:05.076159375Z     all_namespaces = _load_all_namespaces(resolver)
2025-07-06T12:55:05.076162155Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 61, in _load_all_namespaces
2025-07-06T12:55:05.076164525Z     url_patterns = getattr(resolver, "url_patterns", [])
2025-07-06T12:55:05.076167425Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:55:05.076169825Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:55:05.076172515Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:55:05.076190716Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 715, in url_patterns
2025-07-06T12:55:05.076194166Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-07-06T12:55:05.076197096Z                        ^^^^^^^^^^^^^^^^^^^
2025-07-06T12:55:05.076199466Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T12:55:05.076202426Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T12:55:05.076205076Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T12:55:05.076207736Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 708, in urlconf_module
2025-07-06T12:55:05.076210587Z     return import_module(self.urlconf_name)
2025-07-06T12:55:05.076213836Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:55:05.076216347Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:55:05.076218877Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:55:05.076221667Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:55:05.076224607Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:55:05.076227717Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:55:05.076230337Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:55:05.076233117Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:55:05.076252888Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:55:05.076256348Z   File "/opt/render/project/src/payroll/urls.py", line 38, in <module>
2025-07-06T12:55:05.076258938Z     path('admin/payroll/', include('employees.admin_urls', namespace='payroll_admin')),
2025-07-06T12:55:05.076261588Z                            ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:55:05.076267478Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 38, in include
2025-07-06T12:55:05.076270758Z     urlconf_module = import_module(urlconf_module)
2025-07-06T12:55:05.076273428Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T12:55:05.076276198Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T12:55:05.076278668Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:55:05.076281778Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T12:55:05.076284429Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T12:55:05.076286938Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T12:55:05.076289398Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T12:55:05.076291879Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T12:55:05.076294509Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T12:55:05.076297029Z   File "/opt/render/project/src/employees/admin_urls.py", line 2, in <module>
2025-07-06T12:55:05.076299529Z     from . import admin_views
2025-07-06T12:55:05.076302029Z   File "/opt/render/project/src/employees/admin_views.py", line 10, in <module>
2025-07-06T12:55:05.076304499Z     from .forms import OrganizationForm, DepartmentForm
2025-07-06T12:55:05.076307329Z   File "/opt/render/project/src/employees/forms.py", line 9, in <module>
2025-07-06T12:55:05.076317499Z     import pandas as pd
2025-07-06T12:55:05.076320099Z ModuleNotFoundError: No module named 'pandas'