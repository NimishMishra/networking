FROM node:8.12.0-alpine

# Install packages
RUN apk add --update --no-cache supervisor

# Setup app
RUN mkdir -p /app

# Add application
WORKDIR /app
COPY challenge .

# Install dependencies
RUN npm install

# Setup superivsord
COPY config/supervisord.conf /etc/supervisord.conf

# Expose the port node-js is reachable on
EXPOSE 80

# Start the node-js application
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]