# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files (flat style so imports like `import agent_executor` work)
COPY multi_tool_agent/* ./

# Expose both ports
EXPOSE 8000 9999

# Run both servers in background & foreground
CMD ["sh", "-c", "python __main__.py & python agent.py"]
