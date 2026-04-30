# Solution -- Fix the Broken NGINX Container

> Spoiler. Do not read this file before attempting the exercise.

## 1. The Bug

`nginx.conf` inside the image is missing a semicolon at the end of the `listen` directive:

```nginx
server {
    listen       80          # <-- missing ';'
    server_name  localhost;
    ...
}
```

NGINX is strict about its grammar. Every directive **must** end with `;`. Because the parser fails before NGINX can bind to a port, the master process exits immediately and Docker reports the container as `Exited (1)`.

## 2. How to Identify It

```bash
docker pull <registry>/nginx-broken:latest
docker run -d --name broken-nginx -p 8080:80 <registry>/nginx-broken:latest
docker ps -a                # STATUS = Exited (1)
docker logs broken-nginx
```

Expected log output:

```
nginx: [emerg] directive "listen" is not terminated by ";" in /etc/nginx/nginx.conf:18
```

The error message tells you:

- The file:        `/etc/nginx/nginx.conf`
- The line:        `18` (the line nginx prints will match the actual file in your image)
- The directive:   `listen`
- The cause:       missing `;`

## 3. Three Ways to Fix It

### Option A -- Mount a fixed config (cleanest, no rebuild)

Use the `solution/nginx.conf` from this repo and mount it over the broken file at runtime:

```bash
docker rm -f broken-nginx 2>/dev/null || true
docker run -d --name fixed-nginx \
    -p 8080:80 \
    -v "$(pwd)/solution/nginx.conf:/etc/nginx/nginx.conf:ro" \
    <registry>/nginx-broken:latest

curl -I http://localhost:8080
# HTTP/1.1 200 OK
```

### Option B -- Edit inside a throwaway container, then commit

Because the container crashes, you can't `docker exec` into it. Start a shell instead by overriding the entrypoint:

```bash
docker run -it --name fixme --entrypoint sh <registry>/nginx-broken:latest

# inside the container:
vi /etc/nginx/nginx.conf      # add the missing ';' on the listen line
exit

docker commit fixme nginx-fixed:local
docker run -d -p 8080:80 nginx-fixed:local
```

### Option C -- Rebuild the image with the fixed config

```bash
docker build -t nginx-fixed:local ./solution-image
docker run -d -p 8080:80 nginx-fixed:local
```

(Requires copying `solution/nginx.conf` next to a small Dockerfile that does `FROM nginx:alpine` + `COPY nginx.conf /etc/nginx/nginx.conf`.)

## 4. Verify

```bash
docker ps                       # STATUS = Up
curl -s http://localhost:8080   # returns the "You fixed it!" HTML page
```

## 5. Take-aways

- `docker logs <container>` is almost always the first stop when a container crashes on boot.
- A crashing container can still be inspected: `docker run --entrypoint sh <image>` gives you a shell **without** running the broken process.
- Bind-mounting a corrected config (`-v host:container`) is the fastest non-destructive fix and is a common pattern in real ops work.
- `docker commit` turns ad-hoc fixes into a reproducible image, but the *real* fix belongs in the Dockerfile and source-controlled config.
