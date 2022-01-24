FROM python:slim-bullseye

RUN  apt-get update \
     && apt-get install --no-install-recommends -y firefox-esr tini cron curl sudo \
     && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
     selenium \
     python-telegram-bot

# Create app directory
WORKDIR /usr/src/app

COPY speedtest.py config.shlib geckodriver.sh ./

RUN mkdir /export

COPY entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["tini", "--", "docker-entrypoint.sh"]
