# Nginx serves the chat files and forwards API requests to the model container.
FROM nginx:stable-alpine

# Replace the default web server configuration with our proxy routes.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# These files run in the browser; no Node.js build step is needed.
COPY index.html styles.css app.js /usr/share/nginx/html/
