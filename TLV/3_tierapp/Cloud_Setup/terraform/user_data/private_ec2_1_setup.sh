#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip git

# Install Flask and dependencies
pip3 install flask flask-cors requests

# Clone your backend repository
git clone https://github.com/Dimon7128/marcotech.git /home/ubuntu/backend

# Navigate to the backend directory
cd /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/2_Proc

# Install Python dependencies
pip3 install -r requirements.txt

# Start the update_color service
nohup python3 update_color.py &