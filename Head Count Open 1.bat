@echo off
cd ..
cd Sitarganj_BP
call venv\Scripts\activate
REM Open URL in Google Chrome
start "" "chrome.exe" "http://127.0.0.1:8000/"
REM Open the desktop shortcut
start "" "C:\Users\Public\Desktop\IOCL API.lnk"
python manage.py runserver
REM Wait for server to start (adjust time if needed)
timeout /t 5 /nobreak >nul
c:\Users\Public\Desktop\IOCL API.lnk