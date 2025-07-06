2025-07-06T13:12:38.875098611Z         databases=databases,
2025-07-06T13:12:38.875102672Z     )
2025-07-06T13:12:38.875106752Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 88, in run_checks
2025-07-06T13:12:38.875111572Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-07-06T13:12:38.875115522Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 14, in check_url_config
2025-07-06T13:12:38.875119452Z     return check_resolver(resolver)
2025-07-06T13:12:38.875123442Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 24, in check_resolver
2025-07-06T13:12:38.875127262Z     return check_method()
2025-07-06T13:12:38.875131712Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 494, in check
2025-07-06T13:12:38.875135892Z     for pattern in self.url_patterns:
2025-07-06T13:12:38.875139852Z                    ^^^^^^^^^^^^^^^^^
2025-07-06T13:12:38.875143642Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T13:12:38.875160853Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T13:12:38.875164003Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T13:12:38.875166753Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 715, in url_patterns
2025-07-06T13:12:38.875197263Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-07-06T13:12:38.875200603Z                        ^^^^^^^^^^^^^^^^^^^
2025-07-06T13:12:38.875203483Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 57, in __get__
2025-07-06T13:12:38.875206114Z     res = instance.__dict__[self.name] = self.func(instance)
2025-07-06T13:12:38.875208683Z                                          ~~~~~~~~~^^^^^^^^^^
2025-07-06T13:12:38.875211264Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 708, in urlconf_module
2025-07-06T13:12:38.875213694Z     return import_module(self.urlconf_name)
2025-07-06T13:12:38.875217084Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T13:12:38.875219714Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T13:12:38.875222014Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T13:12:38.875224664Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T13:12:38.875227214Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T13:12:38.875243004Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T13:12:38.875245754Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T13:12:38.875248274Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T13:12:38.875251404Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T13:12:38.875253995Z   File "/opt/render/project/src/payroll/urls.py", line 46, in <module>
2025-07-06T13:12:38.875256615Z     path('payroll/', include('payroll_processing.urls', namespace='payroll_processing')),
2025-07-06T13:12:38.875259185Z                      ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T13:12:38.875261835Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 38, in include
2025-07-06T13:12:38.875264265Z     urlconf_module = import_module(urlconf_module)
2025-07-06T13:12:38.875266755Z   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-07-06T13:12:38.875269095Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-07-06T13:12:38.875271735Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T13:12:38.875274215Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-07-06T13:12:38.875276845Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-07-06T13:12:38.875279635Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-07-06T13:12:38.875282235Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-07-06T13:12:38.875284895Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-07-06T13:12:38.875287265Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-07-06T13:12:38.875289535Z   File "/opt/render/project/src/payroll_processing/urls.py", line 5, in <module>
2025-07-06T13:12:38.875292025Z     from . import views
2025-07-06T13:12:38.875294655Z   File "/opt/render/project/src/payroll_processing/views.py", line 12, in <module>
2025-07-06T13:12:38.875303265Z     import xlsxwriter
2025-07-06T13:12:38.875306296Z ModuleNotFoundError: No module named 'xlsxwriter'