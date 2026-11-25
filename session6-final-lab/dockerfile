# Match the Python 3.10 environment used to train the supplied model.
FROM python:3.10-slim

# Run the following instructions from /app inside the container.
WORKDIR /app

# Copy dependencies first so their install layer can be reused when app files change.
COPY requirements.txt ./

# Install dependencies without keeping pip's download cache.
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the API code and trained model into /app.
COPY main.py model.joblib ./

# Start main.py's app with Uvicorn, listening on all container interfaces at port 8000.
CMD ["python3","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]
