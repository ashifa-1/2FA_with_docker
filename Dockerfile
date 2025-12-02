# ---------- Stage 1: Builder (install Python deps) ----------
FROM python:3.11-alpine AS builder

# Work inside /app
WORKDIR /app

# Copy deps list
COPY requirements.txt .

# Install Python packages into /install
RUN pip install --no-cache-dir --progress-bar off --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-alpine

# Set timezone to UTC
ENV TZ=UTC

# Work inside /app
WORKDIR /app

# Install lightweight cron + timezone data using Alpine's package manager (apk)
RUN apk add --no-cache tzdata dcron

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy project code
COPY . .

# Create mount points for volumes
RUN mkdir -p /data /cron

# Busybox/dcron reads cron jobs from /etc/crontabs/root
# We'll use your existing cron/2fa-cron file as the root crontab
COPY cron/2fa-cron /etc/crontabs/root
RUN chmod 0644 /etc/crontabs/root

# Expose FastAPI port
EXPOSE 8080

# Start cron daemon AND FastAPI
# crond -l 2  -> cron in foreground with log level 2 (we send it to background with &)
CMD sh -c "crond -l 2 & uvicorn app.main:app --host 0.0.0.0 --port 8080"
