#!/bin/sh

echo "Running speedrunb0t... Press Ctrl+C to abort."

now=$(date +"%H-%M-%S_%m_%d_%Y")
mkdir -p ./logs

# run until exit code 0; redirect all output to log.txt
until python3 Run.py >> "logs/$now.log" 2>> "logs/$now.error"; do
    # if not exit code 0 output error to shell and restart
    now=$(date +"%H-%M-%S_%m_%d_%Y")
    echo "$now: speedrunb0t crashed with exit code $?.  Respawning..." >&2
    sleep 1
done
