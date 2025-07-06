[11:56:55.942] Running build in Washington, D.C., USA (East) – iad1
[11:56:55.943] Build machine configuration: 2 cores, 8 GB
[11:56:55.984] Cloning github.com/Oragwel/kenyan-payroll-management-system (Branch: main, Commit: c15538c)
[11:56:56.119] Previous build caches not available
[11:56:56.279] Cloning completed: 295.000ms
[11:56:56.632] Running "vercel build"
[11:56:57.070] Vercel CLI 44.2.10
[11:56:57.253] WARN! Due to `builds` existing in your configuration file, the Build and Development Settings defined in your Project Settings will not apply. Learn More: https://vercel.link/unused-build-settings
[11:56:57.692] 🚀 Starting build process for Kenyan Payroll System...
[11:56:57.692] 📦 Installing Python dependencies...
[11:56:58.503] Collecting Django==4.2.7 (from -r requirements.txt (line 6))
[11:56:58.534]   Downloading Django-4.2.7-py3-none-any.whl.metadata (4.1 kB)
[11:56:58.567] Collecting djangorestframework==3.14.0 (from -r requirements.txt (line 7))
[11:56:58.571]   Downloading djangorestframework-3.14.0-py3-none-any.whl.metadata (10 kB)
[11:56:58.696] Collecting reportlab==4.0.4 (from -r requirements.txt (line 16))
[11:56:58.700]   Downloading reportlab-4.0.4-py3-none-any.whl.metadata (1.3 kB)
[11:56:58.729] Collecting weasyprint==60.2 (from -r requirements.txt (line 17))
[11:56:58.734]   Downloading weasyprint-60.2-py3-none-any.whl.metadata (3.7 kB)
[11:56:58.758] Collecting openpyxl==3.1.2 (from -r requirements.txt (line 20))
[11:56:58.761]   Downloading openpyxl-3.1.2-py2.py3-none-any.whl.metadata (2.5 kB)
[11:56:58.796] Collecting xlsxwriter==3.1.9 (from -r requirements.txt (line 21))
[11:56:58.799]   Downloading XlsxWriter-3.1.9-py3-none-any.whl.metadata (2.6 kB)
[11:56:58.908] Collecting pandas==2.1.3 (from -r requirements.txt (line 22))
[11:56:58.911]   Downloading pandas-2.1.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (18 kB)
[11:56:58.928] Collecting xlrd==2.0.1 (from -r requirements.txt (line 23))
[11:56:58.931]   Downloading xlrd-2.0.1-py2.py3-none-any.whl.metadata (3.4 kB)
[11:56:59.099] Collecting Pillow==10.1.0 (from -r requirements.txt (line 26))
[11:56:59.104]   Downloading Pillow-10.1.0-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (9.5 kB)
[11:56:59.123] Collecting python-dateutil==2.8.2 (from -r requirements.txt (line 29))
[11:56:59.126]   Downloading python_dateutil-2.8.2-py2.py3-none-any.whl.metadata (8.2 kB)
[11:56:59.171] Collecting pytz==2023.3 (from -r requirements.txt (line 30))
[11:56:59.175]   Downloading pytz-2023.3-py2.py3-none-any.whl.metadata (22 kB)
[11:56:59.259] Collecting requests==2.31.0 (from -r requirements.txt (line 31))
[11:56:59.263]   Downloading requests-2.31.0-py3-none-any.whl.metadata (4.6 kB)
[11:56:59.280] Collecting six==1.16.0 (from -r requirements.txt (line 32))
[11:56:59.283]   Downloading six-1.16.0-py2.py3-none-any.whl.metadata (1.8 kB)
[11:56:59.309] Collecting django-cors-headers==4.3.1 (from -r requirements.txt (line 35))
[11:56:59.313]   Downloading django_cors_headers-4.3.1-py3-none-any.whl.metadata (16 kB)
[11:56:59.331] Collecting django-csp==3.7 (from -r requirements.txt (line 36))
[11:56:59.335]   Downloading django_csp-3.7-py2.py3-none-any.whl.metadata (2.7 kB)
[11:56:59.522] Collecting cryptography==41.0.7 (from -r requirements.txt (line 37))
[11:56:59.526]   Downloading cryptography-41.0.7-cp37-abi3-manylinux_2_28_x86_64.whl.metadata (5.2 kB)
[11:56:59.547] Collecting django-crispy-forms==2.1 (from -r requirements.txt (line 40))
[11:56:59.552]   Downloading django_crispy_forms-2.1-py3-none-any.whl.metadata (5.0 kB)
[11:56:59.567] Collecting crispy-bootstrap5==0.7 (from -r requirements.txt (line 41))
[11:56:59.571]   Downloading crispy_bootstrap5-0.7-py3-none-any.whl.metadata (3.5 kB)
[11:56:59.593] Collecting gunicorn==21.2.0 (from -r requirements.txt (line 45))
[11:56:59.597]   Downloading gunicorn-21.2.0-py3-none-any.whl.metadata (4.1 kB)
[11:56:59.619] Collecting whitenoise==6.6.0 (from -r requirements.txt (line 46))
[11:56:59.624]   Downloading whitenoise-6.6.0-py3-none-any.whl.metadata (3.7 kB)
[11:56:59.641] Collecting django-environ==0.11.2 (from -r requirements.txt (line 47))
[11:56:59.645]   Downloading django_environ-0.11.2-py2.py3-none-any.whl.metadata (11 kB)
[11:56:59.662] Collecting dj-database-url==2.1.0 (from -r requirements.txt (line 48))
[11:56:59.670]   Downloading dj_database_url-2.1.0-py3-none-any.whl.metadata (11 kB)
[11:56:59.732] Collecting psycopg2-binary==2.9.9 (from -r requirements.txt (line 49))
[11:56:59.738]   Downloading psycopg2_binary-2.9.9-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.4 kB)
[11:56:59.754] Collecting django-ratelimit==4.1.0 (from -r requirements.txt (line 60))
[11:56:59.758]   Downloading django_ratelimit-4.1.0-py2.py3-none-any.whl.metadata (2.3 kB)
[11:56:59.803] Collecting django-axes==6.1.1 (from -r requirements.txt (line 61))
[11:56:59.808]   Downloading django_axes-6.1.1-py3-none-any.whl.metadata (37 kB)
[11:56:59.843] Collecting asgiref<4,>=3.6.0 (from Django==4.2.7->-r requirements.txt (line 6))
[11:56:59.844]   Downloading asgiref-3.9.0-py3-none-any.whl.metadata (9.3 kB)
[11:56:59.862] Collecting sqlparse>=0.3.1 (from Django==4.2.7->-r requirements.txt (line 6))
[11:56:59.865]   Downloading sqlparse-0.5.3-py3-none-any.whl.metadata (3.9 kB)
[11:56:59.917] Collecting pydyf>=0.8.0 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:56:59.920]   Downloading pydyf-0.11.0-py3-none-any.whl.metadata (2.5 kB)
[11:57:00.017] Collecting cffi>=0.6 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.021]   Downloading cffi-1.17.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (1.5 kB)
[11:57:00.036] Collecting html5lib>=1.1 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.039]   Downloading html5lib-1.1-py2.py3-none-any.whl.metadata (16 kB)
[11:57:00.055] Collecting tinycss2>=1.0.0 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.059]   Downloading tinycss2-1.4.0-py3-none-any.whl.metadata (3.0 kB)
[11:57:00.074] Collecting cssselect2>=0.1 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.078]   Downloading cssselect2-0.8.0-py3-none-any.whl.metadata (2.9 kB)
[11:57:00.094] Collecting Pyphen>=0.9.1 (from weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.098]   Downloading pyphen-0.17.2-py3-none-any.whl.metadata (3.2 kB)
[11:57:00.299] Collecting fonttools>=4.0.0 (from fonttools[woff]>=4.0.0->weasyprint==60.2->-r requirements.txt (line 17))
[11:57:00.303]   Downloading fonttools-4.58.5-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl.metadata (106 kB)
[11:57:00.309]      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 106.9/106.9 kB 39.1 MB/s eta 0:00:00
[11:57:00.329] Collecting et-xmlfile (from openpyxl==3.1.2->-r requirements.txt (line 20))
[11:57:00.333]   Downloading et_xmlfile-2.0.0-py3-none-any.whl.metadata (2.7 kB)
[11:57:00.554] Collecting numpy<2,>=1.26.0 (from pandas==2.1.3->-r requirements.txt (line 22))
[11:57:00.558]   Downloading numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
[11:57:00.563]      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.0/61.0 kB 20.8 MB/s eta 0:00:00
[11:57:00.598] Collecting tzdata>=2022.1 (from pandas==2.1.3->-r requirements.txt (line 22))
[11:57:00.602]   Downloading tzdata-2025.2-py2.py3-none-any.whl.metadata (1.4 kB)
[11:57:00.701] Collecting charset-normalizer<4,>=2 (from requests==2.31.0->-r requirements.txt (line 31))
[11:57:00.704]   Downloading charset_normalizer-3.4.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
[11:57:00.726] Collecting idna<4,>=2.5 (from requests==2.31.0->-r requirements.txt (line 31))
[11:57:00.729]   Downloading idna-3.10-py3-none-any.whl.metadata (10 kB)
[11:57:00.837] Collecting urllib3<3,>=1.21.1 (from requests==2.31.0->-r requirements.txt (line 31))
[11:57:00.841]   Downloading urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
[11:57:00.866] Collecting certifi>=2017.4.17 (from requests==2.31.0->-r requirements.txt (line 31))
[11:57:00.869]   Downloading certifi-2025.6.15-py3-none-any.whl.metadata (2.4 kB)
[11:57:01.000] Collecting packaging (from gunicorn==21.2.0->-r requirements.txt (line 45))
[11:57:01.004]   Downloading packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
[11:57:01.045] Collecting typing-extensions>=3.10.0.0 (from dj-database-url==2.1.0->-r requirements.txt (line 48))
[11:57:01.048]   Downloading typing_extensions-4.14.1-py3-none-any.whl.metadata (3.0 kB)
[11:57:01.214] Collecting setuptools (from django-axes==6.1.1->-r requirements.txt (line 61))
[11:57:01.217]   Downloading setuptools-80.9.0-py3-none-any.whl.metadata (6.6 kB)
[11:57:01.246] Collecting pycparser (from cffi>=0.6->weasyprint==60.2->-r requirements.txt (line 17))
[11:57:01.249]   Downloading pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
[11:57:01.274] Collecting webencodings (from cssselect2>=0.1->weasyprint==60.2->-r requirements.txt (line 17))
[11:57:01.277]   Downloading webencodings-0.5.1-py2.py3-none-any.whl.metadata (2.1 kB)
[11:57:01.352] Collecting brotli>=1.0.1 (from fonttools[woff]>=4.0.0->weasyprint==60.2->-r requirements.txt (line 17))
[11:57:01.355]   Downloading Brotli-1.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.5 kB)
[11:57:01.394] Collecting zopfli>=0.1.4 (from fonttools[woff]>=4.0.0->weasyprint==60.2->-r requirements.txt (line 17))
[11:57:01.398]   Downloading zopfli-0.2.3.post1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.9 kB)
[11:57:01.543] Downloading Django-4.2.7-py3-none-any.whl (8.0 MB)
[11:57:01.606]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.0/8.0 MB 131.0 MB/s eta 0:00:00
[11:57:01.612] Downloading djangorestframework-3.14.0-py3-none-any.whl (1.1 MB)
[11:57:01.622]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 140.2 MB/s eta 0:00:00
[11:57:01.628] Downloading reportlab-4.0.4-py3-none-any.whl (1.9 MB)
[11:57:01.641]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 180.6 MB/s eta 0:00:00
[11:57:01.645] Downloading weasyprint-60.2-py3-none-any.whl (268 kB)
[11:57:01.652]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 268.8/268.8 kB 91.8 MB/s eta 0:00:00
[11:57:01.654] Downloading openpyxl-3.1.2-py2.py3-none-any.whl (249 kB)
[11:57:01.660]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 250.0/250.0 kB 61.7 MB/s eta 0:00:00
[11:57:01.664] Downloading XlsxWriter-3.1.9-py3-none-any.whl (154 kB)
[11:57:01.670]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 154.8/154.8 kB 41.4 MB/s eta 0:00:00
[11:57:01.675] Downloading pandas-2.1.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.7 MB)
[11:57:01.759]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.7/11.7 MB 139.4 MB/s eta 0:00:00
[11:57:01.762] Downloading xlrd-2.0.1-py2.py3-none-any.whl (96 kB)
[11:57:01.766]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 96.5/96.5 kB 49.7 MB/s eta 0:00:00
[11:57:01.773] Downloading Pillow-10.1.0-cp312-cp312-manylinux_2_28_x86_64.whl (3.6 MB)
[11:57:01.799]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB 142.0 MB/s eta 0:00:00
[11:57:01.803] Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
[11:57:01.811]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 247.7/247.7 kB 42.8 MB/s eta 0:00:00
[11:57:01.814] Downloading pytz-2023.3-py2.py3-none-any.whl (502 kB)
[11:57:01.823]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 502.3/502.3 kB 75.3 MB/s eta 0:00:00
[11:57:01.827] Downloading requests-2.31.0-py3-none-any.whl (62 kB)
[11:57:01.830]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.6/62.6 kB 28.2 MB/s eta 0:00:00
[11:57:01.832] Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
[11:57:01.840] Downloading django_cors_headers-4.3.1-py3-none-any.whl (12 kB)
[11:57:01.846] Downloading django_csp-3.7-py2.py3-none-any.whl (17 kB)
[11:57:01.852] Downloading cryptography-41.0.7-cp37-abi3-manylinux_2_28_x86_64.whl (4.4 MB)
[11:57:01.882]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.4/4.4 MB 160.4 MB/s eta 0:00:00
[11:57:01.886] Downloading django_crispy_forms-2.1-py3-none-any.whl (31 kB)
[11:57:01.894] Downloading crispy_bootstrap5-0.7-py3-none-any.whl (22 kB)
[11:57:01.898] Downloading gunicorn-21.2.0-py3-none-any.whl (80 kB)
[11:57:01.902]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.2/80.2 kB 45.7 MB/s eta 0:00:00
[11:57:01.907] Downloading whitenoise-6.6.0-py3-none-any.whl (19 kB)
[11:57:01.912] Downloading django_environ-0.11.2-py2.py3-none-any.whl (19 kB)
[11:57:01.917] Downloading dj_database_url-2.1.0-py3-none-any.whl (7.7 kB)
[11:57:01.922] Downloading psycopg2_binary-2.9.9-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
[11:57:01.942]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 164.7 MB/s eta 0:00:00
[11:57:01.947] Downloading django_ratelimit-4.1.0-py2.py3-none-any.whl (11 kB)
[11:57:01.954] Downloading django_axes-6.1.1-py3-none-any.whl (64 kB)
[11:57:01.958]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.4/64.4 kB 31.8 MB/s eta 0:00:00
[11:57:01.961] Downloading asgiref-3.9.0-py3-none-any.whl (23 kB)
[11:57:01.966] Downloading certifi-2025.6.15-py3-none-any.whl (157 kB)
[11:57:01.970]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 157.7/157.7 kB 63.4 MB/s eta 0:00:00
[11:57:01.973] Downloading cffi-1.17.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (479 kB)
[11:57:01.979]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 479.4/479.4 kB 135.6 MB/s eta 0:00:00
[11:57:01.982] Downloading charset_normalizer-3.4.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (148 kB)
[11:57:01.986]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 148.6/148.6 kB 69.4 MB/s eta 0:00:00
[11:57:01.990] Downloading cssselect2-0.8.0-py3-none-any.whl (15 kB)
[11:57:01.997] Downloading fonttools-4.58.5-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl (4.9 MB)
[11:57:02.030]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 158.1 MB/s eta 0:00:00
[11:57:02.034] Downloading html5lib-1.1-py2.py3-none-any.whl (112 kB)
[11:57:02.038]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 112.2/112.2 kB 46.7 MB/s eta 0:00:00
[11:57:02.041] Downloading idna-3.10-py3-none-any.whl (70 kB)
[11:57:02.045]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 70.4/70.4 kB 37.4 MB/s eta 0:00:00
[11:57:02.050] Downloading numpy-1.26.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.0 MB)
[11:57:02.168]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 18.0/18.0 MB 125.3 MB/s eta 0:00:00
[11:57:02.177] Downloading pydyf-0.11.0-py3-none-any.whl (8.1 kB)
[11:57:02.180] Downloading pyphen-0.17.2-py3-none-any.whl (2.1 MB)
[11:57:02.194]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 174.7 MB/s eta 0:00:00
[11:57:02.198] Downloading sqlparse-0.5.3-py3-none-any.whl (44 kB)
[11:57:02.201]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.4/44.4 kB 21.7 MB/s eta 0:00:00
[11:57:02.205] Downloading tinycss2-1.4.0-py3-none-any.whl (26 kB)
[11:57:02.210] Downloading typing_extensions-4.14.1-py3-none-any.whl (43 kB)
[11:57:02.214]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43.9/43.9 kB 24.5 MB/s eta 0:00:00
[11:57:02.218] Downloading tzdata-2025.2-py2.py3-none-any.whl (347 kB)
[11:57:02.224]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 347.8/347.8 kB 90.9 MB/s eta 0:00:00
[11:57:02.227] Downloading urllib3-2.5.0-py3-none-any.whl (129 kB)
[11:57:02.234]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 129.8/129.8 kB 28.8 MB/s eta 0:00:00
[11:57:02.237] Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)
[11:57:02.242] Downloading packaging-25.0-py3-none-any.whl (66 kB)
[11:57:02.246]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.5/66.5 kB 33.1 MB/s eta 0:00:00
[11:57:02.254] Downloading setuptools-80.9.0-py3-none-any.whl (1.2 MB)
[11:57:02.263]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 183.1 MB/s eta 0:00:00
[11:57:02.270] Downloading Brotli-1.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.9 MB)
[11:57:02.292]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.9/2.9 MB 148.7 MB/s eta 0:00:00
[11:57:02.295] Downloading webencodings-0.5.1-py2.py3-none-any.whl (11 kB)
[11:57:02.305] Downloading zopfli-0.2.3.post1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (851 kB)
[11:57:02.311]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 851.1/851.1 kB 167.8 MB/s eta 0:00:00
[11:57:02.314] Downloading pycparser-2.22-py3-none-any.whl (117 kB)
[11:57:02.320]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 117.6/117.6 kB 31.1 MB/s eta 0:00:00
[11:57:02.693] Installing collected packages: webencodings, pytz, brotli, zopfli, xlsxwriter, xlrd, whitenoise, urllib3, tzdata, typing-extensions, tinycss2, sqlparse, six, setuptools, Pyphen, pydyf, pycparser, psycopg2-binary, Pillow, packaging, numpy, idna, fonttools, et-xmlfile, django-ratelimit, django-environ, charset-normalizer, certifi, asgiref, requests, reportlab, python-dateutil, openpyxl, html5lib, gunicorn, Django, cssselect2, cffi, weasyprint, pandas, djangorestframework, django-csp, django-crispy-forms, django-cors-headers, django-axes, dj-database-url, cryptography, crispy-bootstrap5
[11:57:15.507] Successfully installed Django-4.2.7 Pillow-10.1.0 Pyphen-0.17.2 asgiref-3.9.0 brotli-1.1.0 certifi-2025.6.15 cffi-1.17.1 charset-normalizer-3.4.2 crispy-bootstrap5-0.7 cryptography-41.0.7 cssselect2-0.8.0 dj-database-url-2.1.0 django-axes-6.1.1 django-cors-headers-4.3.1 django-crispy-forms-2.1 django-csp-3.7 django-environ-0.11.2 django-ratelimit-4.1.0 djangorestframework-3.14.0 et-xmlfile-2.0.0 fonttools-4.58.5 gunicorn-21.2.0 html5lib-1.1 idna-3.10 numpy-1.26.4 openpyxl-3.1.2 packaging-25.0 pandas-2.1.3 psycopg2-binary-2.9.9 pycparser-2.22 pydyf-0.11.0 python-dateutil-2.8.2 pytz-2023.3 reportlab-4.0.4 requests-2.31.0 setuptools-80.9.0 six-1.16.0 sqlparse-0.5.3 tinycss2-1.4.0 typing-extensions-4.14.1 tzdata-2025.2 urllib3-2.5.0 weasyprint-60.2 webencodings-0.5.1 whitenoise-6.6.0 xlrd-2.0.1 xlsxwriter-3.1.9 zopfli-0.2.3.post1
[11:57:15.508] WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[11:57:15.588] 
[11:57:15.589] [notice] A new release of pip is available: 24.0 -> 25.1.1
[11:57:15.589] [notice] To update, run: python3.12 -m pip install --upgrade pip
[11:57:16.161] 📁 Collecting static files...
[11:57:16.405] Traceback (most recent call last):
[11:57:16.405]   File "/vercel/path0/manage.py", line 22, in <module>
[11:57:16.405]     main()
[11:57:16.406]   File "/vercel/path0/manage.py", line 18, in main
[11:57:16.406]     execute_from_command_line(sys.argv)
[11:57:16.406]   File "/python312/lib/python3.12/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
[11:57:16.406]     utility.execute()
[11:57:16.406]   File "/python312/lib/python3.12/site-packages/django/core/management/__init__.py", line 416, in execute
[11:57:16.406]     django.setup()
[11:57:16.406]   File "/python312/lib/python3.12/site-packages/django/__init__.py", line 24, in setup
[11:57:16.406]     apps.populate(settings.INSTALLED_APPS)
[11:57:16.406]   File "/python312/lib/python3.12/site-packages/django/apps/registry.py", line 116, in populate
[11:57:16.406]     app_config.import_models()
[11:57:16.406]   File "/python312/lib/python3.12/site-packages/django/apps/config.py", line 269, in import_models
[11:57:16.406]     self.models_module = import_module(models_module_name)
[11:57:16.406]                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.406]   File "/python312/lib/python3.12/importlib/__init__.py", line 90, in import_module
[11:57:16.406]     return _bootstrap._gcd_import(name[level:], package, level)
[11:57:16.406]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.407]   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
[11:57:16.407]   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
[11:57:16.407]   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
[11:57:16.407]   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
[11:57:16.407]   File "<frozen importlib._bootstrap_external>", line 995, in exec_module
[11:57:16.407]   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
[11:57:16.407]   File "/python312/lib/python3.12/site-packages/django/contrib/auth/models.py", line 3, in <module>
[11:57:16.407]     from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
[11:57:16.407]   File "/python312/lib/python3.12/site-packages/django/contrib/auth/base_user.py", line 57, in <module>
[11:57:16.407]     class AbstractBaseUser(models.Model):
[11:57:16.408]   File "/python312/lib/python3.12/site-packages/django/db/models/base.py", line 143, in __new__
[11:57:16.408]     new_class.add_to_class("_meta", Options(meta, app_label))
[11:57:16.408]   File "/python312/lib/python3.12/site-packages/django/db/models/base.py", line 371, in add_to_class
[11:57:16.408]     value.contribute_to_class(cls, name)
[11:57:16.409]   File "/python312/lib/python3.12/site-packages/django/db/models/options.py", line 243, in contribute_to_class
[11:57:16.409]     self.db_table, connection.ops.max_name_length()
[11:57:16.409]                    ^^^^^^^^^^^^^^
[11:57:16.409]   File "/python312/lib/python3.12/site-packages/django/utils/connection.py", line 15, in __getattr__
[11:57:16.409]     return getattr(self._connections[self._alias], item)
[11:57:16.409]                    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
[11:57:16.409]   File "/python312/lib/python3.12/site-packages/django/utils/connection.py", line 62, in __getitem__
[11:57:16.409]     conn = self.create_connection(alias)
[11:57:16.409]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.409]   File "/python312/lib/python3.12/site-packages/django/db/utils.py", line 193, in create_connection
[11:57:16.409]     backend = load_backend(db["ENGINE"])
[11:57:16.409]               ^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.410]   File "/python312/lib/python3.12/site-packages/django/db/utils.py", line 113, in load_backend
[11:57:16.410]     return import_module("%s.base" % backend_name)
[11:57:16.410]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.410]   File "/python312/lib/python3.12/importlib/__init__.py", line 90, in import_module
[11:57:16.410]     return _bootstrap._gcd_import(name[level:], package, level)
[11:57:16.410]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[11:57:16.410]   File "/python312/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py", line 9, in <module>
[11:57:16.410]     from sqlite3 import dbapi2 as Database
[11:57:16.410]   File "/python312/lib/python3.12/sqlite3/__init__.py", line 57, in <module>
[11:57:16.413]     from sqlite3.dbapi2 import *
[11:57:16.414]   File "/python312/lib/python3.12/sqlite3/dbapi2.py", line 27, in <module>
[11:57:16.420]     from _sqlite3 import *
[11:57:16.421] ModuleNotFoundError: No module named '_sqlite3'
[11:57:16.483] 📂 Copying static files to output directory...
[11:57:16.484] No static files to copy
[11:57:16.484] ⚠️ No DATABASE_URL found, skipping database operations...
[11:57:16.485] ✅ Build process completed successfully!
[11:57:16.490] Error: The Output Directory "staticfiles_build" is empty.
[11:57:16.490] Learn More: https://vercel.link/missing-public-directory
[11:57:16.774] 
[11:57:19.202] Exiting build container

## Issues Identified and Fixed:

1. **SQLite Module Error**: The Vercel build environment doesn't have SQLite support
   - Fixed by using dummy database backend for build process
   - Updated build.py settings to use 'django.db.backends.dummy'

2. **Missing DATABASE_URL**: No database URL was provided during build
   - Added conditional database configuration in production.py
   - Build script now handles missing DATABASE_URL gracefully

3. **Empty Output Directory**: Static files weren't collected properly
   - Updated build script to ensure static files are copied
   - Added fallback content creation for output directory

4. **Python Runtime**: Updated to Python 3.12 to match build environment

## ✅ Database Setup Complete - Supabase PostgreSQL

Database credentials received from Vercel/Supabase:
- Database Type: Supabase PostgreSQL
- Host: aws-0-us-east-1.pooler.supabase.com
- Database: postgres
- User: postgres.tjfnxsozfmxhcanlhgcc

## 🔧 Environment Variables to Configure in Vercel:

### Required Variables (copy these to Vercel dashboard):

```
DATABASE_URL=postgres://postgres.tjfnxsozfmxhcanlhgcc:rdNGSmdBk6oXS7RS@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=payroll.settings.production
ALLOWED_HOSTS=.vercel.app,.now.sh
```

### Optional Variables:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourcompany.com
```

## 🚀 Next Steps:

1. **Generate Secret Key**:
   ```python
   import secrets
   print(secrets.token_urlsafe(50))
   ```

2. **Configure Environment Variables in Vercel**:
   - Go to your Vercel project dashboard
   - Settings → Environment Variables
   - Add the variables listed above

3. **Deploy**:
   - Changes are already pushed to GitHub
   - Trigger new deployment in Vercel dashboard

## Fixed Files:
- build_files.sh: Updated to handle SQLite absence and use dummy database
- payroll/settings/production.py: Added fallback database config and fixed imports
- vercel.json: Updated Python runtime to 3.12