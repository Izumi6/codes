@echo off
setlocal

REM Get PC name and username
set "PC_NAME=%COMPUTERNAME%"
set "USER_NAME=%USERNAME%"

REM Define output file name
set "OUTPUT_FILE=%PC_NAME%_%USER_NAME%_wifi_passwords.txt"

REM Clear the output file if it exists
echo. > "%OUTPUT_FILE%"

REM Retrieve and save all Wi-Fi profiles and their passwords
for /f "tokens=*" %%i in ('netsh wlan show profiles') do (
    set "line=%%i"
    if "!line:~0,9!"=="All User " (
        set "profile_name=!line:~15!"
        echo Retrieving password for profile: !profile_name!
        netsh wlan show profile "!profile_name!" key=clear | findstr /R /C:"Key Content" >> "%OUTPUT_FILE%"
        echo. >> "%OUTPUT_FILE%"
    )
)

echo All Wi-Fi passwords have been saved to "%OUTPUT_FILE%"

endlocal
pause
