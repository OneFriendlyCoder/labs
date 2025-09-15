#!/bin/bash
set -euo pipefail

PID_FILE="/home/.evaluationScripts/python_processes.pids"
: > "${PID_FILE}"

if ! command -v ping &>/dev/null; then
    apt-get update -qq
    apt-get install -y iputils-ping >/dev/null 2>&1
fi

launch() {
  nohup "$@" >/dev/null 2>&1 &
  echo $! >> "${PID_FILE}"
}

launch python3 /home/.evaluationScripts/tcp_connection_server.py
sleep 5
launch python3 /home/.evaluationScripts/tcp_connection_client.py
launch python3 /home/.evaluationScripts/udp_connection.py

printf "\nAll scripts launched. PIDs saved in %s:\n\n" "${PID_FILE}"
cat "${PID_FILE}"

while read -r pid; do
  echo "Waiting on PID ${pid}..."
  wait "${pid}"
  echo "Process ${pid} has exited."
done < "${PID_FILE}"
