FROM nginx:alpine

RUN apk update
RUN apk upgrade

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d