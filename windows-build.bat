@echo off
SETLOCAL ENABLEEXTENSIONS

:: Check for Python and get version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH.
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv .venv

:: Activate virtual environment
echo Activating virtual environment...
CALL .venv\Scripts\activate.bat

:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Run Nuitka build command
echo Running Nuitka build...
python -m nuitka --standalone --include-data-dir=zenith/media=zenith/media --include-data-files=zenith/shortcuts.lua=zenith/shortcuts.lua --include-data-files=zenith/color_schemes.lua=zenith/color_schemes.lua --enable-plugin=pyqt6 --include-module=PyQt6.Qsci --windows-console-mode=disable --windows-icon-from-ico=zenith/media/icon.ico Nyxtext.py

:: Copy lupa package to Nyxtext.dist
echo Copying lupa package...
xcopy /E /I .venv\Lib\site-packages\lupa Nyxtext.dist\lupa\

echo Process completed.
ENDLOCAL