setlocal enabledelayedexpansion
@echo off
cd /d "%~dp0"
set VENV_PATH=..\..\..\.venv\Scripts
set CORE_PATH=..\..
%VENV_PATH%\python %CORE_PATH%\BaseUtil\UtilRes.py %CORE_PATH%\BaseRes
%VENV_PATH%\pyside6-rcc %CORE_PATH%\resources.qrc -o %CORE_PATH%\BaseUI\BaseRc.py
del %CORE_PATH%\resources.qrc
pause