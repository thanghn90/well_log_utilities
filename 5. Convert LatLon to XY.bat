@echo off
echo %cd%

set MASTERDIR=..

PATH=.;^
%MASTERDIR%\python

set PYTHONPATH=.;^
%MASTERDIR%\pyscripts

:loop_csv
echo.
echo Enter path of latitutde-longitude csv file
set latlon_fn=latlon.csv
set /p latlon_fn="Default is %latlon_fn%: "
if not exist "%latlon_fn%" (
	echo csv file NOT found!
	goto loop_csv
)

python.exe %MASTERDIR%\pyscripts\convert_coordinates.py %latlon_fn%

pause