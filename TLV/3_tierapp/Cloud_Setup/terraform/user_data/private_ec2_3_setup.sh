#!/bin/bash
yum update -y
yum install -y python3 git

# Install Flask and dependencies
pip3 install flask flask-cors requests

# Clone your backend repository
git clone https://github.com/Dimon7128/marcotech.git /home/ubuntu/backend

# Navigate to the backend directory
cd /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/4_Proc
    
# Install Python dependencies
pip3 install -r requirements.txt

# Start the not_allowed_service
nohup python3 not_allowed_service.py &