FROM python:3.6.8-stretch
ENV PYTHONUNBUFFERED 1

WORKDIR /app
#RUN ls /app/server
COPY ./server/bb_server/requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY ./server/backbone_server/REQUIREMENTS /tmp/backbone_requirements.txt
RUN apt-get install -y libpq-dev
RUN pip3 install --no-cache-dir -r /tmp/backbone_requirements.txt
COPY compose/production/backbone_server/requirements.txt /tmp/server_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/server_requirements.txt
COPY ./server .

COPY ./compose/production/backbone_server/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/backbone_server/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


WORKDIR /app/server/bb_server
ENTRYPOINT ["/entrypoint"]
