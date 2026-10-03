# Image: <your-dockerhub-user>/nginx-broken:latest
# Purpose: Intentionally broken NGINX image used for the
# "Fix the Broken NGINX Container" troubleshooting exercise.
#
# The image ships a malformed /etc/nginx/nginx.conf that causes
# nginx to fail at startup. The student is expected to:
#   1. Observe the crash (`docker ps -a`)
#   2. Read the logs  (`docker logs <id>`)
#   3. Fix the config (inside the container, via mount, or rebuild)

FROM nginx:1.27-alpine

LABEL maintainer="marcotech-etgar"
LABEL exercise="broken-nginx-container"
LABEL description="Intentionally broken NGINX image for troubleshooting practice"

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

# Inherit the default CMD from nginx:alpine ("nginx -g 'daemon off;'")
