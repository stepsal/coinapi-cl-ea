FROM tiangolo/uwsgi-nginx:python3.7-alpine3.8

RUN pip install flask requests

ENV LISTEN_PORT 5000
ENV UWSGI_INI /app/uwsgi.ini
ENV PYTHONPATH=/app:/usr/local/lib/python3.7/site-packages:/usr/lib/python3.7/site-packages

COPY ./coinapi_cl_ea.py ./flask_app.py ./__init__.py /app/
WORKDIR /app

# Update the conf file
RUN echo -e '[uwsgi]\n\
module = flask_app\n\
callable = app' > /app/uwsgi.ini && \
echo -e "client_max_body_size 0;" > /etc/nginx/conf.d/upload.conf && \
sed -i "/worker_processes\s/c\worker_processes 1;" /etc/nginx/nginx.conf && \
echo -e "server {\n\
    listen ${LISTEN_PORT};\n\
    location / {\n\
        try_files \$uri @app;\n\
    }\n\
    location @app {\n\
        include uwsgi_params;\n\
        uwsgi_pass unix:///tmp/uwsgi.sock;\n\
    }}" > /etc/nginx/conf.d/nginx.conf

CMD ["/usr/bin/supervisord"]