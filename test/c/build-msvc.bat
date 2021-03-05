@echo off

echo Discovering environment...

set ERRORLEVEL=0
if not exist build mkdir build
if %ERRORLEVEL% NEQ 0 echo "Failed to create build directory." && exit /b %ERRORLEVEL%

python -c "import sys; print(sys.base_exec_prefix)" > build/_PYTHON_BASE
if %ERRORLEVEL% NEQ 0 echo "Failed to get python base directory." && exit /b %ERRORLEVEL%
set /P PYTHON_BASE=<build/_PYTHON_BASE
echo     PYTHON_BASE=%PYTHON_BASE%

python -c "import _woosh; print(_woosh.__file__[:-3] + 'lib')" > build/_WOOSH_LIB
if %ERRORLEVEL% NEQ 0 echo "Failed to get woosh lib." && exit /b %ERRORLEVEL%
set /P WOOSH_LIB=<build/_WOOSH_LIB
echo     WOOSH_LIB=%WOOSH_LIB%


echo Discovering tests to build...

dir /b /s api\test_*.c > build/_API_TESTS
if %ERRORLEVEL% NEQ 0 echo "Failed to find API tests." && exit /b %ERRORLEVEL%
for /f %%f in (build/_API_TESTS) do echo     %%f

dir /b /s internal\test_*.c > build/_INTERNAL_TESTS
if %ERRORLEVEL% NEQ 0 echo "Failed to find internal tests." && exit /b %ERRORLEVEL%
for /f %%f in (build/_INTERNAL_TESTS) do echo     %%f


echo Building API tests...
for /f %%f in (build/_API_TESTS) do (
    echo     Building %%~nf...
    if exist build\%%~nf.exe del /f build\%%~nf.exe
    if exist build\%%~nf.exe echo "Failed to delete test." && exit /b 1
    cl /Fo.\build\ /I ../../inc/ /I "%PYTHON_BASE%/include" api/base.c %%f /link %WOOSH_LIB% /LIBPATH:"%PYTHON_BASE%/libs" /out:build/%%~nf.exe 1>build/%%~nf.log 2>&1
    if not exist build\%%~nf.exe type build\%%~nf.log && echo Failed to build test. && exit /b 1
)

echo Building internal tests...
for /f %%f in (build/_INTERNAL_TESTS) do (
    echo     Building %%~nf...
    if exist build\%%~nf.exe del /f build\%%~nf.exe
    if exist build\%%~nf.exe echo "Failed to delete test." && exit /b 1
    cl /Fo.\build\ /I ../../src/_woosh/ %%f /link /out:build/%%~nf.exe 1>build/%%~nf.log 2>&1
    if not exist build\%%~nf.exe type build\%%~nf.log && echo Failed to build test.  && exit /b 1
)
