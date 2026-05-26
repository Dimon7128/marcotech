#!/bin/bash

# Start update_color.py
echo "Starting update_color.py..."
cd 2_Proc
python3 update_color.py &  # Run update_color.py in the background
update_pid=$!  # Capture its process ID

# Wait for 1 second
sleep 1

# Start query_color.py
echo "Starting query_color.py..."
cd ../3_Proc
python3 query_color.py &  # Run query_color.py in the background
query_pid=$!  # Capture its process ID

# Function to clean up processes
cleanup() {
    pkill -f query_color.py 
    pkill -f update_color.py
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to call cleanup
trap cleanup SIGINT SIGTERM

# Wait for both processes to finish
wait
