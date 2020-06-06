FROM python:3.7.6-alpine3.11

ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app/privileged-api

COPY ./uwsgi.ini /etc/uwsgi.ini

COPY requirements.txt .

RUN apk add --no-cache libffi-dev postgresql-client postgresql-dev linux-headers gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["uwsgi", "--ini", "/etc/uwsgi.ini", "--wsgi-file", "app.py", "--lazy-apps", "--callable", "app"]