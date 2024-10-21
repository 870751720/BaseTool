setlocal enabledelayedexpansion
cd /d "%~dp0"
set VENV_PATH=..\..\..\.venv\Scripts
%VENV_PATH%\python %VENV_PATH%\pywin32_postinstall.py -install
rem pywin32导致了环境问题那么可以执行
rem %VENV_PATH%\python %VENV_PATH%\pywin32_postinstall.py -remove