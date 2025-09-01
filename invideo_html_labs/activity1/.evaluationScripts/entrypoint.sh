#!/bin/bash
set -e
if [ -f "/opt/check.txt" ]; then
    echo "No Need!"
else
    chmod ugo+rw /home/labDirectory/*
    echo "Done" > /opt/check.txt
fi

while true; do
    sleep 10
done
