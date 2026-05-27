# syntax=docker/dockerfile:1.7
#
# Frontend container — nginx serving 3 static files.
# Matches the image base advertised in README ("nginx:alpine").
# Listens on 80 (mapped to host 8080 by docker-compose.yml).

FROM nginx:alpine

# Replace the stock default.conf with our minimal one (try_files fallback,
# light caching for css/js). See ./nginx.conf for the actual rules.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Static assets. Listed explicitly so unrelated files (e.g. README, Dockerfile
# itself) never sneak into the served document root.
COPY index.html style.css app.js /usr/share/nginx/html/

EXPOSE 80

# The base image's default entrypoint already runs:
#   nginx -g "daemon off;"
# so we don't need to override CMD.
