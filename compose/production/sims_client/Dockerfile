FROM node:11.15.0-stretch-slim as build-deps

COPY ./compose/production/sims_client/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/sims_client/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app/client/sims-backbone

RUN npm install
ENTRYPOINT ["/entrypoint"]
