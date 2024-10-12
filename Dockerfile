# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev pkg-config \
    libmariadb-dev libmariadb-dev-compat default-libmysqlclient-dev

# Create a directory for the application
WORKDIR /app

# Copy the requirements file and install the dependencies in a virtual environment
COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Create a directory for the application
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy the Django project code from the current directory
COPY . /app

# Expose the port Django will run on
EXPOSE 8000

# Run the Django application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jaythree.wsgi:application"]