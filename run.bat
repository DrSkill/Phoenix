@echo off
SETLOCAL EnableDelayedExpansion
chcp 65001 > NUL

set PIPENV_VENV_IN_PROJECT=1

python --version > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo Cannot find Python executable, make sure it is installed and added to your PATH.
    pause
    exit /B 0
)

python -c "import pipenv" > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    python -m pip install --user pipenv
)

pipenv --version > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo Adding pipenv to PATH...
    for /F %%p IN ('python -m site --user-site') do set path_pipenv=%%p
    set PATH=!PATH!;!path_pipenv:site-packages=Scripts!
)

if not exist ".venv" ( pipenv --bare install )

REM Do updates
if "%1"=="update" (
    for /F %%b in ( 'git rev-parse --abbrev-ref HEAD' ) do ( echo Pulling last version from %%b... )
    git pull
    pipenv update
    exit /B 0
)

REM Initialisations
del /Q logs\*
set sleep_time=1

REM ERMAHGERD ! MAH FRAVRIT LERP !
:loop

REM Execute the bot
set time_d=%time%
pipenv run python run.py %*
set exit_code=%ERRORLEVEL%
set time_e=%time%

REM Check for the exit code
if %exit_code% equ 1 (
    REM Restart is asked, sleep for a while
    timeout /T %sleep_time%
) else (
    REM Exit with the bot's exit code
    exit /B %exit_code%
)

REM Numbers starting by 0 are interpreted as octal, so we remove leading zeros in hours, minutes and seconds
set /a hour_d=1%time_d:~0,2% %% 100
set /a min_d=1%time_d:~3,2% %% 100
set /a sec_d=1%time_d:~6,2% %% 100

set /a hour_e=1%time_e:~0,2% %% 100
set /a min_e=1%time_e:~3,2% %% 100
set /a sec_e=1%time_e:~6,2% %% 100

REM Compute the execution time
set /a total_d=(%hour_d%*3600)+(%min_d%*60)+%sec_d%
set /a total_e=(%hour_e%*3600)+(%min_e%*60)+%sec_e%

set /a elapsed_time=%total_e%-%total_d%

REM Compute the next sleep time
if %elapsed_time% gtr 45 (
    REM The execution was long enough, reset the sleep time
    set sleep_time=1
) else (
    REM Double the sleep time but cap it to 45
    if %sleep_time% gtr 22 (
        set sleep_time=45
    ) else (
        set /a sleep_time=%sleep_time% * 2
    )
)

goto loop
