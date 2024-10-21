@echo off
call :RequestAdminElevation "%~dpfs0" %* || goto:eof

%~d0
cd %~dp0
call %*

:RequestAdminElevation FilePath %* || goto:eof
setlocal ENABLEDELAYEDEXPANSION & set "_FilePath=%~1"
if NOT EXIST "!_FilePath!" (echo/Read RequestAdminElevation usage information)
set "_FN=_%~ns1" & echo/%TEMP%| findstr /C:"(" >nul && (echo/ERROR: %%TEMP%% path can not contain parenthesis &pause &endlocal &fc;: 2>nul & goto:eof)
set _FN=%_FN:(=%
set _vbspath="%temp:~%\%_FN:)=%.vbs" & set "_batpath=%temp:~%\%_FN:)=%.bat"
fltmc >nul 2>&1 || goto :_getElevation
(if exist %_vbspath% ( del %_vbspath% )) & (if exist %_batpath% ( del %_batpath% ))
endlocal & CD /D "%~dp1" & ver >nul & goto:eof

:_getElevation
echo/Set UAC = CreateObject^("Shell.Application"^) > %_vbspath% || (echo/&echo/Unable to create %_vbspath% & endlocal &md; 2>nul &goto:eof)
echo/UAC.ShellExecute "%_batpath%", "", "", "runas", 1 >> %_vbspath% & echo/wscript.Quit(1)>> %_vbspath%
echo/@%* > "%_batpath%" || (echo/&echo/Unable to create %_batpath% & endlocal &md; 2>nul &goto:eof)
echo/@if %%errorlevel%%==9009 (echo/^&echo/Admin user could not read the batch file. If running from a mapped drive or UNC path, check if Admin user can read it.)^&echo/^& @if %%errorlevel%% NEQ 0 pause >> "%_batpath%"
%_vbspath% && (echo/&echo/Failed to run VBscript %_vbspath% &endlocal &md; 2>nul & goto:eof)
echo/&endlocal &fc;: 2>nul & goto:eof