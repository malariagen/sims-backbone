FROM node:11.15.0-stretch-slim as build

WORKDIR /app

RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install -y libpq-dev git openjdk-8-jre-headless && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/malariagen/sims-backbone.git
RUN (cd sims-backbone;./generate.sh)


FROM python:3.6.8-stretch
ENV PYTHONUNBUFFERED 1

WORKDIR /app/upload

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/sims-backbone/server/bb_server/requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY --from=build /app/sims-backbone/server/backbone_server/REQUIREMENTS /tmp/backbone_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/backbone_requirements.txt

COPY --from=build /app/sims-backbone/python_client/requirements.txt /tmp/python_client_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/python_client_requirements.txt
COPY --from=build /app/sims-backbone/upload/requirements.txt /tmp/upload_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/upload_requirements.txt
RUN pip3 install --no-cache-dir git+https://github.com/idwright/chemistry-cmislib.git

RUN pip3 install --no-cache-dir awscli

COPY --from=build /app/sims-backbone/server/backbone_server/ /app/server/backbone_server/
COPY --from=build /app/sims-backbone/server/bb_server/ /app/server/bb_server/
COPY --from=build /app/sims-backbone/server/overlay/* /app/server/bb_server/
COPY --from=build /app/sims-backbone/upload /app/upload/
COPY --from=build /app/sims-backbone/python_client /app/python_client/

COPY ./compose/production/import/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/import/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


ENTRYPOINT ["/entrypoint"]
