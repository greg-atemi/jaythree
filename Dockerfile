FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . .

EXPOSE 8000

# ENTRYPOINT ["python3", "manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]

RUN python3 manage.py migrate
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jaythree.wsgi:application"]
