FROM python:3.7.6-alpine3.11

ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "Starting worker process..."

CMD ["python", "main.py"]