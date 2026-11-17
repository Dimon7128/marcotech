### LAB 3  |  Read a Dockerfile

**8 minutes  |  After teaching Slide 22**

**Goal:** Understand how Docker packages Python, our application, dependencies and model.

1.  Create a file named Dockerfile (no extension) inside sms-service/. Paste:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY main.py model.joblib ./
CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]
```

2.  Find the instruction that installs libraries and the instruction that copies the trained model.

3.  Identify what starts the API when the container runs. Why must Uvicorn listen on 0.0.0.0 inside Docker?

> **CHECK:** Point to FROM, RUN, COPY and CMD and explain each instruction in one sentence.

> **Instructor note:** Use a base image with the same compatible Python version as Session 4. Change python:3.11-slim if Session 4 used a different version.

### LAB 4  |  Build the image

**8 minutes  |  After teaching Slide 23**

**Goal:** Turn the Dockerfile and application files into a tagged image.

1.  Confirm Docker is running, then open a terminal in the folder containing your Dockerfile.

2.  Build the image (the final dot means “use this folder as the build context”).

```bash
docker build -t sms-api:1.0 .
```

3.  Check that Docker lists the image and its version tag.

```bash
docker images
```

> **CHECK:** The image list contains repository sms-api with tag 1.0.

> **Think about it:** Does docker build start a running web API, or only create the packaged image?

### LAB 5  |  Run and test the container

**9 minutes  |  After teaching Slide 23**

**Goal:** Run the packaged service and compare it with the local API.

1.  Leave your local API on port 8000 if it is still running. Start the container using host port 8001:

```bash
docker run --rm -p 8001:8000 sms-api:1.0
```

2.  Open http://localhost:8001/health and confirm HTTP 200 with {"status":"ok"}.

3.  Open http://localhost:8001/docs. Test POST /predict with:

```json
{"message": "Meeting at 5 today"}
```

4.  Try one invalid request, such as {"message":""}. Confirm HTTP 422.

5.  Compare: local API = localhost:8000; Docker API = localhost:8001. Stop the running container with Ctrl+C.

> **CHECK:** The container responds at port 8001. /health → 200, valid /predict → 200 and label, invalid /predict → 422.

> **Think about it:** Did we need to retrain the classifier to run it inside Docker?

## Fast fixes

- ModuleNotFoundError — Activate the virtual environment and reinstall requirements.txt; check the Docker build output.
- model.joblib not found — Verify file location and name; place it beside main.py and rebuild the Docker image.
- Model cannot load — Match the Python, scikit-learn and related dependency versions used when the model was saved.
- Port already in use — Stop the conflicting service, or change the host port (left side of -p).
- Docker unavailable — Complete Labs 1–2 locally; follow Labs 3–5 in an instructor-led demonstration.
### Handoff to Session 6

Keep main.py, model.joblib, requirements.txt and Dockerfile. The next lesson can automate the image build and basic API tests with CI/CD.

> **FINAL CHECK:** Students can explain request → FastAPI → saved pipeline → prediction, and reproduce the service locally or in Docker.
