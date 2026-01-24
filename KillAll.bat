@echo off
echo Killing all Lisabella processes...
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
echo Done. You can close this window.
pause
