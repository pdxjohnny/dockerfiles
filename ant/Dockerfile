FROM alpine:edge

ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:$JAVA_HOME/bin

ENV JAVA_VERSION 8u92
ENV JAVA_ALPINE_VERSION 8.92.14-r0

RUN set -x && \
    apk --no-cache add \
        openjdk8="$JAVA_ALPINE_VERSION" \
        apache-ant \
        bash

ENTRYPOINT ["ant"]
