@echo off

mkdir build 2> nul

python -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)" > build/_WOOSH_DLL_DIR
set /P WOOSH_DLL_DIR=<build/_WOOSH_DLL_DIR
set PATH=%WOOSH_DLL_DIR%;%PATH%

set retval=0

dir /b /s test_*.exe > build/_TESTS
for /F "tokens=*" %%t in (build/_TESTS) do %%t || if %errorlevel%==0 set retval=1

exit /b %retval%
