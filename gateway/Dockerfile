FROM debian:9

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y -q \
  && DEBIAN_FRONTEND=noninteractive apt-get -yq install build-essential libssl-dev curl \
  && curl -sL https://deb.nodesource.com/setup_9.x |  bash - \
  && DEBIAN_FRONTEND=noninteractive apt-get -yq install nodejs git vim

RUN mkdir /app
WORKDIR /app

RUN npm install iota.lib.js randbytes

ADD iota-gw-service.js /app/

ENTRYPOINT [ "node", "iota-gw-service.js" ]

