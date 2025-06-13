#!/bin/bash
# Update package lists
apt-get update
apt-get install -y nginx git

# Clone your backend repository
git clone https://github.com/Dimon7128/marcotech.git /home/ubuntu/frontend

# Copy the frontend files to the correct location
cp /home/ubuntu/frontend/TLV/3_tierapp/Cloud_Setup/1_Proc/main.html /home/ubuntu/
cp /home/ubuntu/frontend/TLV/3_tierapp/Cloud_Setup/1_Proc/update_not_allowed.html /home/ubuntu/

# Set proper permissions
chown -R ubuntu:ubuntu /home/ubuntu
chmod 755 /home/ubuntu/main.html
chmod 755 /home/ubuntu/update_not_allowed.html

# Configure Nginx with correct root directory
cat << EOF > /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /home/ubuntu;
    index main.html;

    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location /api/update_color {
        proxy_pass http://${update_color_ip}:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api/get_color {
        proxy_pass http://${query_color_ip}:5002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api/update_not_allowed {
        proxy_pass http://${not_allowed_ip}:5003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api/get_not_allowed {
        proxy_pass http://${not_allowed_ip}:5003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Restart Nginx
systemctl restart nginx
