# Use a specific Python version
ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=whisper.settings

# Set the working directory inside the container
WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy requirements file separately to leverage caching
COPY requirements.txt .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the rest of the application code
COPY whisper/ .

EXPOSE 8000

# Switch to the non-privileged user to run the application
USER appuser

# Command to run the application (ensure DJANGO_SETTINGS_MODULE is set)
CMD ["python3", "manage.py", "runserver"]
