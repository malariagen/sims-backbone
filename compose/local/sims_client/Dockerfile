FROM node:11.15.0-stretch-slim as build-deps

COPY ./compose/local/sims_client/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/local/sims_client/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app/client/sims-backbone

RUN npm install -g @angular/cli@7
RUN npm install "@types/node"@"^12.6.9" --no-optional --no-package-lock
RUN npm install typescript@">=3.4.0  <3.6.0" --no-optional --no-package-lock

ENTRYPOINT ["/entrypoint"]
