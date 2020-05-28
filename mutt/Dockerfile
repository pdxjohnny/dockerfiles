# Usage
# docker build .
# docker run --rm -ti -p 80:8080 intelotc/operations -insecure -log debug
FROM ubuntu:16.04 as mutt

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
  apt-get install -y \
    mutt \
    krb5-user \
    ca-certificates && \
  rm -rf /var/lib/apt/lists/*

RUN useradd -m user

WORKDIR /home/user

RUN mkdir -p /var/mail/user && \
  chown user:user -R /var/mail/user && \
  chown user:user -R /home/user

USER user

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
