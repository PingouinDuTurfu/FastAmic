FROM rabbitmq:4.1.2-management

COPY ./rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["rabbitmq-server"]
