@echo off

REM Run pyinstaller
pyinstaller --onefile -i "logo.png" --noconsole MyWLGUI.py

REM Rename the output file
ren dist\MyWLGUI.exe WLpercentages.exe

REM Clean up build files
rmdir /s /q build
del /s /q __pycache__
del GUI_Example.spec
copy logo.png dist/logo.png

echo WLpercentages.exe has been created.