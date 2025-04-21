FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.2 \
    UVICORN_PORT=8000 \
    PYTHONPATH=/app/src  

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application source code
COPY src ./src

# Expose the application port
EXPOSE 8000

# Start the FastAPI server
CMD ["poetry", "run", "uvicorn", "boilerplate.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
