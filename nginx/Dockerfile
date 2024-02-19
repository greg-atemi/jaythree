FROM nginx:1.23-alpine

# Removing default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copying our nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
