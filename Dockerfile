FROM alpine:3.15

# Create app directory
WORKDIR /usr/src/app

#RUN \
#    echo '@edge http://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories && \
#    echo '@edge http://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories

RUN apk update && apk add --no-cache \
    gcc \
    sed \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    py3-pip \
    bash \
    firefox-esr \
    libressl-dev \
    musl-dev \
    libffi-dev \
    curl \
    jq \
    tini

RUN rm -rf /var/cache/apk/*

RUN pip3 install --no-cache-dir \
     selenium \
     python-telegram-bot

COPY speedtest.py config.shlib geckodriver.sh ./

RUN mkdir /export

COPY entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["tini", "--", "docker-entrypoint.sh"]
