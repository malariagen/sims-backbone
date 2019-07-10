FROM python:3.6.8-stretch
ENV PYTHONUNBUFFERED 1

WORKDIR /app/bb_server

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY ./server/bb_server/requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY ./server/backbone_server/REQUIREMENTS /tmp/backbone_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/backbone_requirements.txt
COPY compose/production/backbone_server/requirements.txt /tmp/server_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/server_requirements.txt

COPY ./compose/production/backbone_server/entrypoint /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/backbone_server/start /start
RUN chmod +x /start


COPY ./server /app
COPY ./compose/production/backbone_server/__init__.py /app/bb_server/openapi_server/__init__.py

ENTRYPOINT ["/entrypoint"]
