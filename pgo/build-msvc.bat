@echo off

set dir=%~dp0

python -m venv "%dir%\_pgoenv"

call _pgoenv\scripts\activate.bat

cd ..
python setup.py build_ext --pgo-generate -f --pgo-data "%dir%\woosh.pgd" install
cd "%dir%"

for /f %%i in ('python -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)"') do set extension_location=%%i
echo %extension_location%
copy "%dir%\woosh.pgd" "%extension_location%\woosh.pgd"

python generate-pgo-data.py

cd ..
python setup.py build_ext --pgo-use --pgo-data "%extension_location%\woosh.pgd" -f
cd "%dir%"

call _pgoenv\scripts\deactivate.bat