@echo off
REM Batch download script for NASA OCO-2 L2 Lite FP (.nc4) files
REM Requires wget installed in PATH, an authenticated cookie.txt, and file_list.txt

set "OUTDIR=.\data\raw_nc4"
set "URL_LIST=file_list.txt"
set "COOKIE_FILE=cookie.txt"

if not exist "%URL_LIST%" (
    echo Error: %URL_LIST% not found. Please place your NASA GES DISC download URL list in the root directory.
    pause
    exit /b 1
)

if not exist "%COOKIE_FILE%" (
    echo Error: %COOKIE_FILE% not found. Please prepare your NASA Earthdata authentication cookie file.
    pause
    exit /b 1
)

if not exist "%OUTDIR%" (
    echo Output directory does not exist. Creating: %OUTDIR%
    mkdir "%OUTDIR%"
)

for /f "usebackq tokens=*" %%A in ("%URL_LIST%") do (
    echo Downloading: %%A
    echo Saving to: %OUTDIR%
    REM wget options:
    REM   --load-cookies / --save-cookies / --keep-session-cookies : Earthdata session authentication
    REM   -c : Resume partially downloaded files
    REM   -P : Target output directory
    wget --load-cookies="%COOKIE_FILE%" --save-cookies="%COOKIE_FILE%" --keep-session-cookies -c -P "%OUTDIR%" "%%A"
    if errorlevel 1 (
        echo Download failed: %%A
    ) else (
        echo Download succeeded: %%A
    )
)

echo All download tasks completed. Please check files in %OUTDIR%.
pause
