FROM python:3.7.6-alpine3.11

ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN apk add --no-cache libffi-dev  linux-headers gcc musl-dev g++ && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./uwsgi.ini /etc/uwsgi.ini

EXPOSE 5000

RUN echo "Starting Location API..."

CMD ["uwsgi", "--ini", "/etc/uwsgi.ini", "--lazy-apps", "--callable", "app"]