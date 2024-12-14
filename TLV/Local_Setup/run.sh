#!/bin/bash

# Navigate to the 2_Proc directory and run update_color.py
echo "Starting update_color.py..."
cd 2_Proc
python3 update_color.py &  # Run update_color.py in the background
update_pid=$!  # Capture the process ID of update_color.py

# Wait for 1 second
sleep 1

# Navigate to the 3_Proc directory and run query_color.py
echo "Starting query_color.py..."
cd ../3_Proc
python3 query_color.py &  # Run query_color.py in the background
query_pid=$!  # Capture the process ID of query_color.py

# Wait for both processes to terminate (optional)
wait $update_pid $query_pid
