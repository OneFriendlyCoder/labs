#!/bin/bash
set -euo pipefail

PID_FILE="/home/.evaluationScripts/python_processes.pids"
: > "${PID_FILE}"

launch() {
  nohup "$@" >/dev/null 2>&1 &
  echo $! >> "${PID_FILE}"
  # don’t disown: we want to be able to wait on them
}

launch /home/.evaluationScripts/spin_server.py

while read -r pid; do
  echo "Waiting on PID ${pid}..."
  wait "${pid}"
  echo "Process ${pid} has exited."
done < "${PID_FILE}"