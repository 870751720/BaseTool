setlocal enabledelayedexpansion
@echo off
cd /d "%~dp0"
set VENV_PATH=..\..\..\.venv\Scripts
set CORE_PATH=..\..
%VENV_PATH%\python %CORE_PATH%\base_util\util_res.py %CORE_PATH%\base_res
%VENV_PATH%\pyside6-rcc %CORE_PATH%\resources.qrc -o %CORE_PATH%\base_ui\base_rc.py
del %CORE_PATH%\resources.qrc