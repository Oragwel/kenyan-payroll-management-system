2025-07-06T17:52:26.082031072Z Collecting python-dateutil==2.8.2 (from -r requirements.txt (line 13))
2025-07-06T17:52:26.084339433Z   Using cached python_dateutil-2.8.2-py2.py3-none-any.whl.metadata (8.2 kB)
2025-07-06T17:52:26.140834439Z Collecting pytz==2023.3 (from -r requirements.txt (line 14))
2025-07-06T17:52:26.142837533Z   Using cached pytz-2023.3-py2.py3-none-any.whl.metadata (22 kB)
2025-07-06T17:52:26.196026301Z Collecting openpyxl==3.1.2 (from -r requirements.txt (line 17))
2025-07-06T17:52:26.198402894Z   Using cached openpyxl-3.1.2-py2.py3-none-any.whl.metadata (2.5 kB)
2025-07-06T17:52:26.473345684Z Collecting Pillow==10.1.0 (from -r requirements.txt (line 20))
2025-07-06T17:52:26.475351388Z   Using cached Pillow-10.1.0.tar.gz (50.8 MB)
2025-07-06T17:52:27.797166836Z   Installing build dependencies: started
2025-07-06T17:52:28.861746867Z   Installing build dependencies: finished with status 'done'
2025-07-06T17:52:28.862946829Z   Getting requirements to build wheel: started
2025-07-06T17:52:29.255781522Z   Getting requirements to build wheel: finished with status 'error'
2025-07-06T17:52:29.262519051Z   error: subprocess-exited-with-error
2025-07-06T17:52:29.262553772Z   
2025-07-06T17:52:29.262559192Z   × Getting requirements to build wheel did not run successfully.
2025-07-06T17:52:29.262563653Z   │ exit code: 1
2025-07-06T17:52:29.262568382Z   ╰─> [21 lines of output]
2025-07-06T17:52:29.262572383Z       Traceback (most recent call last):
2025-07-06T17:52:29.262577013Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 389, in <module>
2025-07-06T17:52:29.262580903Z           main()
2025-07-06T17:52:29.262584633Z           ~~~~^^
2025-07-06T17:52:29.262588553Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 373, in main
2025-07-06T17:52:29.262593143Z           json_out["return_val"] = hook(**hook_input["kwargs"])
2025-07-06T17:52:29.262596913Z                                    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T17:52:29.262601454Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 143, in get_requires_for_build_wheel
2025-07-06T17:52:29.262621354Z           return hook(config_settings)
2025-07-06T17:52:29.262623924Z         File "/tmp/pip-build-env-1jlyfkup/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 331, in get_requires_for_build_wheel
2025-07-06T17:52:29.262626274Z           return self._get_build_requires(config_settings, requirements=[])
2025-07-06T17:52:29.262628404Z                  ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T17:52:29.262631754Z         File "/tmp/pip-build-env-1jlyfkup/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 301, in _get_build_requires
2025-07-06T17:52:29.262634034Z           self.run_setup()
2025-07-06T17:52:29.262636254Z           ~~~~~~~~~~~~~~^^
2025-07-06T17:52:29.262639184Z         File "/tmp/pip-build-env-1jlyfkup/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 317, in run_setup
2025-07-06T17:52:29.262641364Z           exec(code, locals())
2025-07-06T17:52:29.262643484Z           ~~~~^^^^^^^^^^^^^^^^
2025-07-06T17:52:29.262645625Z         File "<string>", line 30, in <module>
2025-07-06T17:52:29.262648025Z         File "<string>", line 27, in get_version
2025-07-06T17:52:29.262650215Z       KeyError: '__version__'
2025-07-06T17:52:29.262652445Z       [end of output]
2025-07-06T17:52:29.262654685Z   
2025-07-06T17:52:29.262657325Z   note: This error originates from a subprocess, and is likely not a problem with pip.
2025-07-06T17:52:29.273326319Z error: subprocess-exited-with-error
2025-07-06T17:52:29.27335422Z 
2025-07-06T17:52:29.27335861Z × Getting requirements to build wheel did not run successfully.
2025-07-06T17:52:29.27336137Z │ exit code: 1
2025-07-06T17:52:29.27336489Z ╰─> See above for output.
2025-07-06T17:52:29.273367661Z 
2025-07-06T17:52:29.27337095Z note: This error originates from a subprocess, and is likely not a problem with pip.
2025-07-06T17:52:29.524713431Z ==> Build failed 😞
2025-07-06T17:52:29.524742092Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys