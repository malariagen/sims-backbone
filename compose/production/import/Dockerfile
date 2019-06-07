FROM python:3.6.8-stretch
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get install -y libpq-dev
#RUN ls /app/server
COPY ./server/bb_server/requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY ./server/backbone_server/REQUIREMENTS /tmp/backbone_requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/backbone_requirements.txt

COPY python_client/requirements.txt /tmp/python_client_requirements.txt
RUN pip3 install -r /tmp/python_client_requirements.txt
COPY test/requirements.txt /tmp/test_requirements.txt
RUN pip3 install -r /tmp/test_requirements.txt
COPY upload/requirements.txt /tmp/upload_requirements.txt
RUN pip3 install -r /tmp/upload_requirements.txt
RUN pip3 install git+https://github.com/idwright/chemistry-cmislib.git
#COPY ./server .
#COPY ./server/overlay/* ./server/bb_server/
#COPY ./server/backbone_server ./server/bb_server/

WORKDIR /app/upload
COPY ./compose/production/import/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/import/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


