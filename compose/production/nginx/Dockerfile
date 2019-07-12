FROM node:11.15.0-stretch-slim as build

WORKDIR /app

ARG BUILD_AS
ARG BACKBONE_API_LOCATION
ARG SIMS_REDIRECT_URI

ENV PATH /app/node_modules/.bin:$PATH

RUN apt-get update
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y git openjdk-8-jre-headless
RUN git clone https://github.com/malariagen/sims-backbone.git
RUN (cd sims-backbone;./generate.sh client)
RUN mv sims-backbone/client/sims-backbone/* .

RUN npm install -g @angular/cli@7
RUN npm install "@types/node"@"^10.14.6" --no-optional --no-package-lock
RUN rm /app/projects/malariagen/sims/package-lock.json
RUN cd /app/projects/malariagen/sims;npm install
RUN cd /app/projects/malariagen/sims;npm install typescript@">=3.1.1 <3.3" --no-optional --no-package-lock
RUN cd /app/projects/malariagen/sims;npm run build
RUN rm -rf /app/projects/malariagen/sims/node_modules
#RUN cd /app/dist/malariagen/sims;npm link
RUN rm /app/package-lock.json
RUN npm install
RUN npm install typescript@">=3.1.1 <3.3" --no-optional --no-package-lock

COPY ./client/sims-backbone/src/environments/environment.prod.ts /app/src/environments/environment.prod.ts

#RUN ng build -c $BUILD_AS
RUN ng build sims-backbone --delete-output-path=false -c $BUILD_AS


FROM nginx:1.14.1-alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;"]
