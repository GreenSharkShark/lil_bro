FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/niginx/conf.d
COPY proxy_params /etc/nginx