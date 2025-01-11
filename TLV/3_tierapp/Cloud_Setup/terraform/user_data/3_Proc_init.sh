#!/bin/bash
yum update -y
yum install -y python3 git

# Install Flask and dependencies
pip3 install flask flask-cors requests

# Clone your backend repository
git clone https://github.com/yourusername/your-backend-repo.git /home/ec2-user/backend

# Navigate to the backend directory
cd /home/ec2-user/backend

# Install Python dependencies
pip3 install -r requirements.txt

# Start the query_color service
nohup python3 query_color.py &