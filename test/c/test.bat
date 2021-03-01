
python -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)" > _WOOSH_DLL_DIR
set /P WOOSH_DLL_DIR=<_WOOSH_DLL_DIR
set PATH=%WOOSH_DLL_DIR%;%PATH%

set retval=0

dir /b /s test_*.exe > _tests
for /F "tokens=*" %%t in (_tests) do %%t || if %errorlevel%==0 set retval=1

exit /b %retval%
