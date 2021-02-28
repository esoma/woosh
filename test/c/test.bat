
set retval=0

dir /b /s test_*.exe > tests
for /F "tokens=*" %%t in (tests) do %%t || if %errorlevel%==0 set retval=1

exit /b %retval%
