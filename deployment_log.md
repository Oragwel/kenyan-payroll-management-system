2025-07-06T12:39:32.187904049Z Collecting django-crispy-forms==2.1 (from -r requirements.txt (line 9))
2025-07-06T12:39:32.189021291Z   Using cached django_crispy_forms-2.1-py3-none-any.whl.metadata (5.0 kB)
2025-07-06T12:39:32.206797082Z Collecting python-dateutil==2.8.2 (from -r requirements.txt (line 12))
2025-07-06T12:39:32.207891172Z   Using cached python_dateutil-2.8.2-py2.py3-none-any.whl.metadata (8.2 kB)
2025-07-06T12:39:32.246994709Z Collecting pytz==2023.3 (from -r requirements.txt (line 13))
2025-07-06T12:39:32.248163573Z   Using cached pytz-2023.3-py2.py3-none-any.whl.metadata (22 kB)
2025-07-06T12:39:32.404933013Z Collecting Pillow==10.1.0 (from -r requirements.txt (line 16))
2025-07-06T12:39:32.406240004Z   Using cached Pillow-10.1.0.tar.gz (50.8 MB)
2025-07-06T12:39:33.340590287Z   Installing build dependencies: started
2025-07-06T12:39:34.065201676Z   Installing build dependencies: finished with status 'done'
2025-07-06T12:39:34.065817009Z   Getting requirements to build wheel: started
2025-07-06T12:39:34.3477468Z   Getting requirements to build wheel: finished with status 'error'
2025-07-06T12:39:34.353988881Z   error: subprocess-exited-with-error
2025-07-06T12:39:34.354003772Z   
2025-07-06T12:39:34.354008922Z   × Getting requirements to build wheel did not run successfully.
2025-07-06T12:39:34.354013453Z   │ exit code: 1
2025-07-06T12:39:34.354018033Z   ╰─> [21 lines of output]
2025-07-06T12:39:34.354022083Z       Traceback (most recent call last):
2025-07-06T12:39:34.354026543Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 389, in <module>
2025-07-06T12:39:34.354030334Z           main()
2025-07-06T12:39:34.354034114Z           ~~~~^^
2025-07-06T12:39:34.354038004Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 373, in main
2025-07-06T12:39:34.354042714Z           json_out["return_val"] = hook(**hook_input["kwargs"])
2025-07-06T12:39:34.354046624Z                                    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:39:34.354050815Z         File "/opt/render/project/src/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 143, in get_requires_for_build_wheel
2025-07-06T12:39:34.354054585Z           return hook(config_settings)
2025-07-06T12:39:34.354058405Z         File "/tmp/pip-build-env-f6jpljj7/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 331, in get_requires_for_build_wheel
2025-07-06T12:39:34.354073816Z           return self._get_build_requires(config_settings, requirements=[])
2025-07-06T12:39:34.354076756Z                  ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-07-06T12:39:34.354079666Z         File "/tmp/pip-build-env-f6jpljj7/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 301, in _get_build_requires
2025-07-06T12:39:34.354082337Z           self.run_setup()
2025-07-06T12:39:34.354084706Z           ~~~~~~~~~~~~~~^^
2025-07-06T12:39:34.354087727Z         File "/tmp/pip-build-env-f6jpljj7/overlay/lib/python3.13/site-packages/setuptools/build_meta.py", line 317, in run_setup
2025-07-06T12:39:34.354090057Z           exec(code, locals())
2025-07-06T12:39:34.354092387Z           ~~~~^^^^^^^^^^^^^^^^
2025-07-06T12:39:34.354094727Z         File "<string>", line 30, in <module>
2025-07-06T12:39:34.354096997Z         File "<string>", line 27, in get_version
2025-07-06T12:39:34.354099267Z       KeyError: '__version__'
2025-07-06T12:39:34.354101527Z       [end of output]
2025-07-06T12:39:34.354103768Z   
2025-07-06T12:39:34.354106578Z   note: This error originates from a subprocess, and is likely not a problem with pip.
2025-07-06T12:39:34.362943211Z error: subprocess-exited-with-error
2025-07-06T12:39:34.362955742Z 
2025-07-06T12:39:34.362959712Z × Getting requirements to build wheel did not run successfully.
2025-07-06T12:39:34.362962642Z │ exit code: 1
2025-07-06T12:39:34.362965492Z ╰─> See above for output.
2025-07-06T12:39:34.362967942Z 
2025-07-06T12:39:34.362970952Z note: This error originates from a subprocess, and is likely not a problem with pip.
2025-07-06T12:39:34.513136001Z ==> Build failed 😞
2025-07-06T12:39:34.513148541Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys