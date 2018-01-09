#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1

python3 --version > /dev/null 2>&1
if [ $? != 0 ]
then
    echo Cannot find Python3 executable, make sure it is installed and added to your PATH.
    read -p "Press [Enter] to exit..."
    exit 0
fi

python3 -c "import pipenv" > /dev/null 2>&1
if [ $? != 0 ]
then
    python3 -m pip install --user pipenv
fi

pipenv --version > /dev/null 2>&1
if [ $? != 0 ]
then
    pipenv_path=$(python3 -m site --user-base)/bin
    PATH+=:$pipenv_path
fi

if [ ! -d '.venv' ]
then
    pipenv --bare install
fi

pipenv run python3 -c "exit(__import__('discord').opus.is_loaded())" > /dev/null 2>&1
if [ $? == 0 ]
then
    echo Cannot find libopus on your system, make sure it is installed.
    read -p "Press [Enter] to exit..."
    exit 0
fi

if [ "$1" == 'update' ]
then
    branch=$(git rev-parse --abbrev-ref HEAD)
    echo Pulling last version from "${branch}"...
    git pull
    pipenv update
    exit 0
fi

rm logs/*
sleep_time=1

# ERMAHGERD ! MAH FRAVRIT LERP !
while true
do
    # Execute the bot
    start_time=$(date +%s)
    pipenv run python3 run.py "$@"
    exit_code=$?
    end_time=$(date +%s)

    # Check for the exit code
    if [ $exit_code -eq 1 ]
    then
        # Restart is asked, sleep for a while
        sleep $sleep_time
    else
        # Exit with the bot's exit code
        exit $exit_code
    fi

    # Compute the next sleep time
    if [ $((end_time - start_time)) -ge 45 ]
    then
        # The execution was long enough, reset the sleep time
        sleep_time=1
    else
        # Double the sleep time but cap it to 45
        sleep_time=$((sleep_time > 22 ? 45 : sleep_time * 2))
    fi
done
