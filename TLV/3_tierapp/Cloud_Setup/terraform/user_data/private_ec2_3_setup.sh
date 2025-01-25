#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip git

# Install Flask and dependencies
pip3 install flask flask-cors requests

# Clone your backend repository
git clone https://github.com/Dimon7128/marcotech.git /home/ubuntu/backend

# Create environment file
cat << EOF > /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/4_Proc/.env
UPDATE_COLOR_IP=${update_color_ip}
EOF

# Navigate to the backend directory
cd /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/4_Proc
    
# Install Python dependencies
pip3 install -r requirements.txt python-dotenv

# Start the not_allowed_service with environment variables
export UPDATE_COLOR_IP=${update_color_ip}
nohup python3 not_allowed_service.py &