FROM python:3.12-slim

LABEL maintainer="marcotech-etgar"
LABEL exercise="broken-compose-stack"
LABEL component="web"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
