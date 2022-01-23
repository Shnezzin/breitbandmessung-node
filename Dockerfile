FROM alpine:3.15

# Create app directory
WORKDIR /usr/src/app

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    python3 \
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

COPY geckodriver.sh .
RUN ./geckodriver.sh

RUN pip3 install \
     selenium \
     python-telegram-bot

COPY speedtest.py config.shlib ./

RUN mkdir /export

COPY entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["tini", "--", "docker-entrypoint.sh"]
