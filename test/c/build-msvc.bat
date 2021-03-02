
mkdir build

python -c "import sys; print(sys.base_exec_prefix)" > build/_PYTHON_BASE
set /P PYTHON_BASE=<build/_PYTHON_BASE

python -c "import _woosh; print(_woosh.__file__[:-3] + 'lib')" > build/_WOOSH_LIB
set /P WOOSH_LIB=<build/_WOOSH_LIB

cl /Fo.\build\ /I ../../src/ ../../src/fifobuffer.c internal/test_fifobuffer.c /link /out:build/test_fifobuffer.exe
cl /Fo.\build\ /I ../../src/ ../../src/lifobuffer.c internal/test_lifobuffer.c /link /out:build/test_lifobuffer.exe
cl /Fo.\build\ /I ../../inc/ /I "%PYTHON_BASE%/include" api/base.c api/test_module_get.c /link %WOOSH_LIB% /LIBPATH:"%PYTHON_BASE%/libs" /out:build/test_module_get.exe
