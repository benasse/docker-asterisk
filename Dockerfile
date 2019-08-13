FROM ubuntu:bionic
MAINTAINER Benoît Stahl <from@b5.pm>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get install --yes git curl wget libnewt-dev libssl-dev \
        libncurses5-dev subversion  libsqlite3-dev build-essential libjansson-dev libxml2-dev  uuid-dev && \
    apt-get install --yes aptitude-common libboost-filesystem1.65.1 libboost-iostreams1.65.1 \
        libboost-system1.65.1 libcgi-fast-perl libcgi-pm-perl libclass-accessor-perl \
        libcwidget3v5 libencode-locale-perl libfcgi-perl libhtml-parser-perl \
        libhtml-tagset-perl libhttp-date-perl libhttp-message-perl libio-html-perl \
        libio-string-perl liblwp-mediatypes-perl libparse-debianchangelog-perl \
        libsigc++-2.0-0v5 libsub-name-perl libtimedate-perl liburi-perl libxapian30 && \
    apt-get install --yes --no-install-recommends python3-requests

WORKDIR /usr/src/asterisk

RUN curl -s http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-16-current.tar.gz \
    | tar -xvz -C /usr/src/ && mv /usr/src/asterisk-*/* /usr/src/asterisk/ && \
    /usr/src/asterisk/contrib/scripts/get_mp3_source.sh && \
    /usr/src/asterisk/contrib/scripts/install_prereq install && \
    ./configure && \
    make menuselect.makeopts && \
    menuselect/menuselect --enable codec_opus --disable BUILD_NATIVE menuselect.makeopts

RUN make && make install && make config && ldconfig

RUN curl -s  https://raw.githubusercontent.com/benasse/docker-asterisk/master/download_g729.py | python3 /dev/stdin --asterisk-version 16

RUN apt-get remove --yes git curl wget libnewt-dev libssl-dev \
        libncurses5-dev subversion  libsqlite3-dev build-essential libjansson-dev libxml2-dev  uuid-dev && \
    apt-get remove --yes aptitude-common libboost-filesystem1.65.1 libboost-iostreams1.65.1 \
        libboost-system1.65.1 libcgi-fast-perl libcgi-pm-perl libclass-accessor-perl \
        libcwidget3v5 libencode-locale-perl libfcgi-perl libhtml-parser-perl \
        libhtml-tagset-perl libhttp-date-perl libhttp-message-perl libio-html-perl \
        libio-string-perl liblwp-mediatypes-perl libparse-debianchangelog-perl \
        libsigc++-2.0-0v5 libsub-name-perl libtimedate-perl liburi-perl libxapian30 && \
    apt-get remove --yes python3-requests && apt-get autoremove --yes && \
    rm -rf /var/lib/apt/lists/*

COPY configs/ /etc/asterisk/
COPY startup.sh /root/startup.sh

EXPOSE 5060/udp
EXPOSE 10000-10100/udp

ENTRYPOINT ["/bin/bash", "/root/startup.sh"]
