@echo off
echo %cd%

set MASTERDIR=..

PATH=.;^
%MASTERDIR%\python

set PYTHONPATH=.;^
%MASTERDIR%\pyscripts

:loop_uid
echo.
set /p uid="Enter chosen well UID: "
if %uid%=="" (
	echo Empty well UID!
	goto loop_uid
)

:loop_csv
echo.
echo Enter path of x-y csv file
set xy_fn=xy.csv
set /p xy_fn="Default is %xy_fn%: "
if not exist "%xy_fn%" (
	echo csv file NOT found!
	goto loop_csv
)

echo.
echo Nearby well search radius (m)
set radius=10000
set /p radius="Default is %radius%: "


python.exe %MASTERDIR%\pyscripts\nearby_wells.py %uid% %xy_fn% %radius%

pause