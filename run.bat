@echo off
echo Starting Cross Post App...
call C:\Users\anikk\anaconda3\Scripts\activate.bat C:\Users\anikk\anaconda3
python main.py
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Please check the output above.
    pause
)
