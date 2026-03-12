# Stage 1: Build dependencies
FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.10-slim

RUN groupadd -r agentuser && useradd -r -g agentuser agentuser

WORKDIR /home/agentuser/app

COPY --from=builder /root/.local /home/agentuser/.local
COPY . .

# Set permissions for the start script
RUN chmod +x start.sh && chown -R agentuser:agentuser /home/agentuser

ENV PATH=/home/agentuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER agentuser

# Entrypoint executes the orchestrator script
CMD ["./start.sh"]
