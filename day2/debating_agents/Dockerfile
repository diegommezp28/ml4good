FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml requirements.lock ./

# Install dependencies using uv with --system flag and lock file
RUN uv pip install --system -r requirements.lock

# Copy the rest of the application
COPY . .

# Set PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "debating_agents.app.main:app", "--host", "0.0.0.0", "--port", "8000"] 