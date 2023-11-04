FROM mysql
COPY *.sql /docker-entrypoint-initdb.d/
RUN echo -e 'mysql -h $HOST --user=${APPUSER} --password=${PASSWORD} SSO' > /usr/bin/prod && \
    chmod +x /usr/bin/prod
