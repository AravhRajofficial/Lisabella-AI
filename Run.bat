@echo off
Title Lisabella Launcher
echo Starting Lisabella AI...
cd /d "%~dp0"

:: Start GUI (Hidden Console using pythonw)
start "" ".venv\Scripts\pythonw.exe" "Frontend\GUI.py"

:: Start Brain (Visible Console)
start "" ".venv\Scripts\python.exe" "Main.py"

exit
