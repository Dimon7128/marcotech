server {
    listen 80;

    location / {
        root /home/ubuntu/1_Proc;
        index main.html;
    }

    # Update color requests go to VM2 where DB.csv is
    location /api/update_color {
        proxy_pass http://${update_color_ip}:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Get color requests go to VM3
    location /api/get_color {
        proxy_pass http://${query_color_ip}:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Update these locations to point to VM4
    location /api/update_not_allowed {
        proxy_pass http://${not_allowed_ip}:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/get_not_allowed {
        proxy_pass http://${not_allowed_ip}:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}