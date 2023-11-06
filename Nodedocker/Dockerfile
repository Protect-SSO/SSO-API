FROM node:18-bullseye-slim as base 
RUN apt-get update -y  \
  && apt-get install -y git
RUN git clone https://github.com/davidkenesaw/SSO-website.git /SSO
WORKDIR /SSO
RUN npm ci
WORKDIR /SSO/Server
ENTRYPOINT [ "node", "app"]
