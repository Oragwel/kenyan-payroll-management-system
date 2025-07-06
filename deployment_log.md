2025-07-06T17:16:35.762974657Z       [11/151] Compiling C object pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/meson-generated_pandas__libs_tslibs_base.pyx.c.o
2025-07-06T17:16:35.762977127Z       FAILED: pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/meson-generated_pandas__libs_tslibs_base.pyx.c.o
2025-07-06T17:16:35.762981128Z       cc -Ipandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p -Ipandas/_libs/tslibs -I../../pandas/_libs/tslibs -I../../../../pip-build-env-3hkfu6o3/overlay/lib/python3.13/site-packages/numpy/core/include -I../../pandas/_libs/include -I/usr/local/include/python3.13 -fvisibility=hidden -fdiagnostics-color=always -DNDEBUG -D_FILE_OFFSET_BITS=64 -w -std=c99 -O3 -DNPY_NO_DEPRECATED_API=0 -DNPY_TARGET_VERSION=NPY_1_21_API_VERSION -fPIC -MD -MQ pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/meson-generated_pandas__libs_tslibs_base.pyx.c.o -MF pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/meson-generated_pandas__libs_tslibs_base.pyx.c.o.d -o pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/meson-generated_pandas__libs_tslibs_base.pyx.c.o -c pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c
2025-07-06T17:16:35.762995729Z       pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c: In function ‘__Pyx_PyInt_As_long’:
2025-07-06T17:16:35.762998579Z       pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c:5397:27: error: too few arguments to function ‘_PyLong_AsByteArray’
2025-07-06T17:16:35.763000739Z        5397 |                 int ret = _PyLong_AsByteArray((PyLongObject *)v,
2025-07-06T17:16:35.763002939Z             |                           ^~~~~~~~~~~~~~~~~~~
2025-07-06T17:16:35.76300503Z       In file included from /usr/local/include/python3.13/longobject.h:107,
2025-07-06T17:16:35.76300715Z                        from /usr/local/include/python3.13/Python.h:81,
2025-07-06T17:16:35.76300928Z                        from pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c:6:
2025-07-06T17:16:35.76301142Z       /usr/local/include/python3.13/cpython/longobject.h:111:17: note: declared here
2025-07-06T17:16:35.76301354Z         111 | PyAPI_FUNC(int) _PyLong_AsByteArray(PyLongObject* v,
2025-07-06T17:16:35.76301563Z             |                 ^~~~~~~~~~~~~~~~~~~
2025-07-06T17:16:35.76301778Z       pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c: In function ‘__Pyx_PyInt_As_int’:
2025-07-06T17:16:35.763019941Z       pandas/_libs/tslibs/base.cpython-313-x86_64-linux-gnu.so.p/pandas/_libs/tslibs/base.pyx.c:5631:27: error: too few arguments to function ‘_PyLong_AsByteArray’
2025-07-06T17:16:35.763021991Z        5631 |                 int ret = _PyLong_AsByteArray((PyLongObject *)v,
2025-07-06T17:16:35.763024081Z             |                           ^~~~~~~~~~~~~~~~~~~
2025-07-06T17:16:35.763026111Z       /usr/local/include/python3.13/cpython/longobject.h:111:17: note: declared here
2025-07-06T17:16:35.763028171Z         111 | PyAPI_FUNC(int) _PyLong_AsByteArray(PyLongObject* v,
2025-07-06T17:16:35.763030192Z             |                 ^~~~~~~~~~~~~~~~~~~
2025-07-06T17:16:35.763032282Z       [12/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/ccalendar.pyx
2025-07-06T17:16:35.763034392Z       [13/151] Compiling C object pandas/_libs/tslibs/parsing.cpython-313-x86_64-linux-gnu.so.p/.._src_parser_tokenizer.c.o
2025-07-06T17:16:35.763039752Z       [14/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/np_datetime.pyx
2025-07-06T17:16:35.763041962Z       [15/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/nattype.pyx
2025-07-06T17:16:35.763044073Z       [16/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/dtypes.pyx
2025-07-06T17:16:35.763046173Z       [17/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/conversion.pyx
2025-07-06T17:16:35.763048343Z       [18/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/tzconversion.pyx
2025-07-06T17:16:35.763050423Z       [19/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/fields.pyx
2025-07-06T17:16:35.763052443Z       [20/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/parsing.pyx
2025-07-06T17:16:35.763054514Z       [21/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/offsets.pyx
2025-07-06T17:16:35.763056544Z       [22/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/strptime.pyx
2025-07-06T17:16:35.763058584Z       [23/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/vectorized.pyx
2025-07-06T17:16:35.763060634Z       [24/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/timezones.pyx
2025-07-06T17:16:35.763062684Z       [25/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/period.pyx
2025-07-06T17:16:35.763066675Z       [26/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/timestamps.pyx
2025-07-06T17:16:35.763068855Z       [27/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/tslibs/timedeltas.pyx
2025-07-06T17:16:35.763071025Z       [28/151] Compiling Cython source /tmp/pip-install-ihmkasw6/pandas_21ce3a324ef046fca452b4a814be6aac/pandas/_libs/algos.pyx
2025-07-06T17:16:35.763073195Z       ninja: build stopped: subcommand failed.
2025-07-06T17:16:35.763075265Z       [end of output]
2025-07-06T17:16:35.763077345Z   
2025-07-06T17:16:35.763079456Z   note: This error originates from a subprocess, and is likely not a problem with pip.
2025-07-06T17:16:35.768905554Z error: metadata-generation-failed
2025-07-06T17:16:35.768916415Z 
2025-07-06T17:16:35.768919005Z × Encountered error while generating package metadata.
2025-07-06T17:16:35.768921465Z ╰─> See above for output.
2025-07-06T17:16:35.768924386Z 
2025-07-06T17:16:35.768930736Z note: This is an issue with the package mentioned above, not pip.
2025-07-06T17:16:35.768934266Z hint: See above for details.
2025-07-06T17:16:36.007686765Z ==> Build failed 😞
2025-07-06T17:16:36.007702396Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys