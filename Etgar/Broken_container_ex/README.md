# Exercise -- Fix the Broken NGINX Container

You are given a prebuilt Docker image that ships an intentionally broken NGINX configuration. Your job is to figure out **why** the container is crashing and **fix** it so the web server runs and serves traffic on port `80`.

> The image used in class is published as `<your-dockerhub-user>/nginx-broken:latest`. Instructors: see [Building the Broken Image](#building-the-broken-image-instructors) at the bottom to publish your own copy.

---

## Objective

1. Identify why the container is crashing.
2. Investigate and fix the issue.
3. Ensure the container runs successfully after applying your fix.

## Steps

1. **Pull the image.**
   ```bash
   docker pull <your-dockerhub-user>/nginx-broken:latest
   ```

2. **Run the container.**
   ```bash
   docker run -d --name broken-nginx -p 8080:80 <your-dockerhub-user>/nginx-broken:latest
   ```

3. **Observe the behavior.** What does `docker ps` show? `docker ps -a`?
   ```bash
   docker ps
   docker ps -a
   ```

4. **Investigate the crash.**
   - Check the logs:
     ```bash
     docker logs broken-nginx
     ```
   - The error message will tell you the exact file, line number, and directive that is wrong.
   - You can also start a shell in a copy of the image (since the original container exited) by overriding the entrypoint:
     ```bash
     docker run -it --rm --entrypoint sh <your-dockerhub-user>/nginx-broken:latest
     # then inside:
     cat /etc/nginx/nginx.conf
     ```

5. **Fix the issue.** Choose any one of these approaches:
   - **Mount a corrected config from the host** (cleanest):
     ```bash
     docker rm -f broken-nginx
     docker run -d --name fixed-nginx -p 8080:80 \
         -v "$(pwd)/my-nginx.conf:/etc/nginx/nginx.conf:ro" \
         <your-dockerhub-user>/nginx-broken:latest
     ```
   - **Edit inside a throwaway container, then `docker commit`** to a new image.
   - **Build a new image** that does `FROM <your-dockerhub-user>/nginx-broken:latest` and `COPY` a corrected `nginx.conf` over the bad one.

6. **Verify.**
   ```bash
   docker ps                       # STATUS should be "Up"
   curl -I http://localhost:8080   # expect HTTP/1.1 200 OK
   ```
   Then open `http://localhost:8080` in a browser. You should see a "You fixed it!" page.

## Deliverables

Submit a short write-up containing:

1. **Diagnosis** -- the exact `docker logs` output and what it told you.
2. **Fix** -- which of the three approaches above you used, and the corrected `nginx.conf` (or `Dockerfile`) you produced.
3. **Proof of success** -- the output of `docker ps` and `curl -I http://localhost:8080` after the fix.

The full reference solution is in [`solution/SOLUTION.md`](solution/SOLUTION.md). Try to solve it yourself first.

---

## Repository Layout

```
Broken_container_ex/
├── README.md                  # this file (exercise instructions)
├── build.sh                   # builds + optionally pushes the broken image
├── nginx-broken/              # source of the broken image
│   ├── Dockerfile
│   ├── nginx.conf             # contains the intentional bug
│   └── index.html             # served once the bug is fixed
└── solution/
    ├── nginx.conf             # corrected config
    └── SOLUTION.md            # walkthrough -- spoiler!
```

---

## Building the Broken Image (instructors)

The exercise ships its own broken image so you don't depend on a third-party Docker Hub account.

```bash
# Build locally as <yourdockerhub>/nginx-broken:latest
./build.sh yourdockerhub

# Build and push to Docker Hub (you must be logged in: `docker login`)
PUSH=1 ./build.sh yourdockerhub latest
```

`build.sh` also runs a quick smoke test that confirms the freshly built image **does** crash with the expected log message -- if it ever stops crashing, the exercise is broken (in a different way).

### Manual build, if you prefer

```bash
docker build -t yourdockerhub/nginx-broken:latest ./nginx-broken
docker push  yourdockerhub/nginx-broken:latest
```

### Confirming the bug is in place

After building, run:

```bash
docker run --rm yourdockerhub/nginx-broken:latest
```

You should see something like:

```
nginx: [emerg] directive "listen" is not terminated by ";" in /etc/nginx/nginx.conf:18
```

That is exactly what the student is supposed to discover.
