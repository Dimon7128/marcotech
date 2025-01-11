#!/bin/bash
yum update -y
yum install -y python3 git

# Install Flask and dependencies
pip3 install flask flask-cors

# Clone your application repository
git clone https://github.com/yourusername/your-repo.git /home/ec2-user/app

# Navigate to the app directory
cd /home/ec2-user/app

# Install Python dependencies
pip3 install -r requirements.txt

# Start the Flask application
nohup python3 app.py &