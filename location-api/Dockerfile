FROM python:3.7.6-alpine3.11

ENV PYTHONBUFFERED 1

RUN mkdir /location_api

WORKDIR /location_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

RUN echo "Starting Location API..."

CMD ["uwsgi", "--ini", "/etc/uwsgi.ini", "--lazy-apps"]