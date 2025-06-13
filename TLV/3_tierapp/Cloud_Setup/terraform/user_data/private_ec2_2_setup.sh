#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip git

# Install Flask and dependencies
pip3 install flask flask-cors requests

# Clone your backend repository
git clone https://github.com/Dimon7128/marcotech.git /home/ubuntu/backend

# Create environment file
cat << EOF > /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/3_Proc/.env
UPDATE_COLOR_IP=${update_color_ip}
EOF

# Navigate to the backend directory
cd /home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/3_Proc

# Install Python dependencies
pip3 install -r requirements.txt python-dotenv

# Create systemd service file
cat <<'SERVICE' > /etc/systemd/system/python-app.service
[Unit]
Description=Query Color Service (Port 5002)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/backend/TLV/3_tierapp/Cloud_Setup/3_Proc
ExecStart=/usr/bin/python3 query_color.py
Environment="PORT=5002"
Environment="UPDATE_COLOR_IP=${update_color_ip}"
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