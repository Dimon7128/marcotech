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

# Create systemd service file
cat <<'SERVICE' > /etc/systemd/system/python-app.service
[Unit]
Description=Update Color Service (Port 5001)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/2_Proc
ExecStart=/usr/bin/python3 update_color.py
Environment="PORT=5001"
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

# Set permissions
chmod 644 /etc/systemd/system/python-app.service

# Reload systemd
systemctl daemon-reload

# Enable and start service
systemctl enable python-app
systemctl start python-app