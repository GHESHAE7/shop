FROM python:3.12.13-alpine3.23

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY . /app

CMD sh -c 'python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000'
