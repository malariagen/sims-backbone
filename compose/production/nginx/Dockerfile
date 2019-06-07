FROM node:11.15.0-stretch-slim as build

WORKDIR /app

ARG BUILD_AS

ENV PATH /app/node_modules/.bin:$PATH

COPY ./client/sims-backbone .

RUN npm install

RUN npm install -g @angular/cli@7.3.9

#RUN ng build -c $BUILD_AS
RUN ng build


FROM nginx:1.14.1-alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;"]
