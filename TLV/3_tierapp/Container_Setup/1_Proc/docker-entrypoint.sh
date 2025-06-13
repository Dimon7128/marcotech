#!/bin/sh

# Replace environment variables in the nginx configuration template
envsubst '$QUERY_COLOR_SERVICE $NOT_ALLOWED_SERVICE $UPDATE_COLOR_SERVICE' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx
exec nginx -g 'daemon off;'