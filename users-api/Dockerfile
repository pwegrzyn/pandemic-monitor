FROM python:3.7.6-alpine3.11

WORKDIR /usr/src/app/users-api
COPY requirements.txt .
COPY ./uwsgi.ini /etc/uwsgi.ini
RUN apk add --no-cache libffi-dev postgresql-client postgresql-dev linux-headers gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT uwsgi --ini /etc/uwsgi.ini --wsgi-file app.py --callable app
