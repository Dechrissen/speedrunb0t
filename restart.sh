#!/bin/sh

echo "Running bot. Press ctrl+c to quit"

# run until exit code 0; redirect all output to log.txt
until python3 Run.py >> log.txt 2>&1; do
    # if not exit code 0 output error to shell and restart
    echo "Bot crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
