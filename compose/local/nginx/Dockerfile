FROM nginx:1.14.1-alpine

COPY ./compose/local/nginx/default.conf /etc/nginx/conf.d

CMD [ "nginx", "-g", "daemon off;"]
