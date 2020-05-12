FROM python:3.6.8-stretch
ENV PYTHONUNBUFFERED 1

WORKDIR /app
#RUN ls /app/server
COPY ./server/bb_server/requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY ./server/backbone_server/REQUIREMENTS /tmp/backbone_requirements.txt
RUN apt-get update && apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev libpq-dev
RUN pip3 install --no-cache-dir -r /tmp/backbone_requirements.txt

#COPY ./server .
#COPY ./server/overlay/* ./server/bb_server/
#COPY ./server/backbone_server ./server/bb_server/

WORKDIR /app/server/bb_server
COPY ./compose/local/backbone_server/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/local/backbone_server/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


ENTRYPOINT ["/entrypoint"]
