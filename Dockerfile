# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron + timezone data
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy project code
COPY . .

# Create mount points
RUN mkdir -p /data /cron

# Install cron job
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

EXPOSE 8080

CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
