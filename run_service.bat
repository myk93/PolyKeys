@echo off
REM Install required Python packages from requirements.txt
pip install -r requirements.txt

REM Check if installation was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements. Exiting.
    exit /b %ERRORLEVEL%
)

REM Run the service_listener.py script
python service_listener.py

REM Check if the script ran successfully
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to run service_listener.py. Exiting.
    exit /b %ERRORLEVEL%
)

echo Service is running...
