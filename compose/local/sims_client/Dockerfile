FROM node:11.15.0-stretch-slim as build-deps

COPY ./compose/local/sims_client/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/local/sims_client/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app/client/sims-backbone

RUN npm install -g @angular/cli@7
RUN npm install "@types/node"@"^10.14.6" --no-optional --no-package-lock
RUN npm install typescript@">=3.1.1 <3.3" --no-optional --no-package-lock

ENTRYPOINT ["/entrypoint"]
