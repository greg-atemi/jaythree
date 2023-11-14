# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
# Base image which is lighter slim, alpine
FROM python:3.7
WORKDIR /jaythree

# ENV PYTHONBUFFERED
# ENV PYTHONBYTECODE
# Allows docker to cache installed dependencies between builds
COPY requirements.txt /jaythree/

RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . .


EXPOSE 8000

# runs the production server
ENTRYPOINT ["python3", "jaythree/manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]