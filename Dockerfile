FROM python:3.8

RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb

RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils

RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_98.0.4758.102-1_amd64.deb
RUN dpkg -i google-chrome-stable_98.0.4758.102-1_amd64.deb; apt-get -fy install

ARG TAP_NAME=''
ARG TAP_FOLDER=TAP_NAME

COPY $TAP_FOLDER /opt/app/$TAP_FOLDER
COPY setup.cfg setup.py tap_entrypoint.sh Dockerfile /opt/app/

WORKDIR /opt/app/

RUN pip install -e .

ENV CONF_LOCATION='' SCHEMA_FILE='' TAP_NAME=$TAP_NAME

RUN  chmod a+x /opt/app/tap_entrypoint.sh

ENTRYPOINT ["/bin/sh", "/opt/app/tap_entrypoint.sh"]