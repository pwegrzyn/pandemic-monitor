FROM redis:5.0.8-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

COPY entrypoint.sh .

RUN chmod 777 ./entrypoint.sh

CMD ["sh", "./entrypoint.sh"]