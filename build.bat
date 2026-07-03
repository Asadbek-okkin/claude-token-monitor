@echo off
echo ================================
echo  Claude Token Monitor - Builder
echo ================================
pip install -r requirements.txt
pip install pyinstaller
python make_icon.py
pyinstaller ^
  --onefile ^
  --windowed ^
  --icon=icon.ico ^
  --name="ClaudeTokenMonitor" ^
  --add-data="icon.ico;." ^
  main.py
echo.
echo Tayyor! dist\ClaudeTokenMonitor.exe
pause
