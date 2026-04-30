#!/bin/bash

# Ensure the script runs from its own directory
cd "$(dirname "$0")" || exit

# 1. Start the server in the background (&)
echo "Starting navigation map editor on port 7070..."
python3 server.py &

# Save the Process ID (PID) of the server so we can track it
SERVER_PID=$!

# 2. Wait a second to ensure the server is up
sleep 2

# 3. Open the browser (Linux standard command)
# 3. Open the browser (Linux standard command)
echo "Opening browser..."
chromium \
  --kiosk "http://localhost:7070/editor.html?v=$(date +%s)" \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-extensions \
  --disable-background-networking \
  --disable-sync \
  --no-first-run \
  --renderer-process-limit=1 \
  --js-flags="--max-old-space-size=128"

# 4. When browser closes, kill the server
kill $SERVER_PID