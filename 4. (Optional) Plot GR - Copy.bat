echo %cd%

set MASTERDIR=..

PATH=.;^
%MASTERDIR%\python

set PYTHONPATH=.;^
%MASTERDIR%\pyscripts

@echo off
set /p uid="Copy and paste desired well UID from Excel here: "

python.exe %MASTERDIR%\pyscripts\plot_gr.py input_list.txt curve_table_GR.csv %uid%

pause