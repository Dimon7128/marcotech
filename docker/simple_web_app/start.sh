#!/bin/sh

# Replace placeholder in the HTML file with the actual instance name
sed -i "s/{{ INSTANCE_NAME }}/$INSTANCE_NAME/" /usr/share/nginx/html/index.html

# Start Nginx
nginx -g 'daemon off;'
