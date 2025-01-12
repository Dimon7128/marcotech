#!/bin/bash
# Update package lists
sudo apt-get update -y

# Install Nginx
sudo apt-get install -y nginx

# Deploy Nginx configuration
sudo bash -c "echo '${replace(local.nginx_config, "\n", "\n")}' > /etc/nginx/sites-available/default"

# Start and enable Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
