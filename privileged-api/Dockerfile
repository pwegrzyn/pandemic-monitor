FROM python:3.7.6-alpine3.11

ENV PYTHONBUFFERED 1

RUN apk --update add libffi-dev postgresql-client postgresql-dev linux-headers gcc musl-dev

RUN mkdir /privileged_api

WORKDIR /privileged_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

RUN echo "Starting Privileged Users API..."

CMD ["uwsgi", "--ini", "/etc/uwsgi.ini", "--lazy-apps"]