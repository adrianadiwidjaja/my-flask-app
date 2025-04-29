#!/bin/bash

# setup.sh - Initialization script with injection for testing purposes

LOG_FILE="logging.txt"
PAYLOAD="# --- Injected Payload for Testing Purposes ---\n# echo 'This file has been modified for testing.'\n"

echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Starting setup and injection process" >> "$LOG_FILE"

# Find and inject payload into .py, .sh, and .js files
for file in $(find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \)); do
    echo -e "$PAYLOAD" >> "$file"
    echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected payload into $file" >> "$LOG_FILE"
done

# Finish setup
echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Setup complete" >> "$LOG_FILE"
