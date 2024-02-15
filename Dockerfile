FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /jaythree
COPY requirements.txt /jaythree/

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . .

EXPOSE 8005

ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8005"]