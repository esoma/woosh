python -c "import sys; print(sys.base_exec_prefix)" > _PYTHON_BASE
set /P PYTHON_BASE=<_PYTHON_BASE

python -c "import _woosh; print(_woosh.__file__[:-3] + 'lib')" > _WOOSH_LIB
set /P WOOSH_LIB=<_WOOSH_LIB

cl /I ../../src/ ../../src/fifobuffer.c test_fifobuffer.c /link /out:test_fifobuffer.exe
cl /I ../../src/ ../../src/lifobuffer.c test_lifobuffer.c /link /out:test_lifobuffer.exe
cl /I ../../inc/ /I "%PYTHON_BASE%/include" capi_test_base.c test_module_get.c /link %WOOSH_LIB% /LIBPATH:"%PYTHON_BASE%/libs" /out:test_module_get.exe
