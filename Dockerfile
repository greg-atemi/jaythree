FROM python:3.10-alpine
WORKDIR /jaythree

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /jaythree/

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . .

EXPOSE 8005
