@echo off

set dir=%~dp0

python -m venv "%dir%\_pgoenv"

call _pgoenv\scripts\activate.bat

python setup.py build_ext --pgo-generate -f --pgo-data "%dir%\_woosh_cpytoken.pgd" install

for /f %%i in ('python -c "import _woosh_cpytoken; import pathlib; print(pathlib.Path(_woosh_cpytoken.__file__).parent)"') do set extension_location=%%i
echo %extension_location%
copy "%dir%\_woosh_cpytoken.pgd" "%extension_location%\_woosh_cpytoken.pgd"

python generate-pgo-data.py

python setup.py build_ext --pgo-use --pgo-data "%extension_location%\_woosh_cpytoken.pgd" -f

call _pgoenv\scripts\deactivate.bat