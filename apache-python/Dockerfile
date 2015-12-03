# VERSION:                0.1
# DESCRIPTION:            Apache and pyhton with mod_cgi
# AUTHOR:                 John Andersen <johnandersenpdx@gmail.com>
# COMMENTS:
#   This file builds a container which runs python scripts with apache mod_cgi
# USAGE:
#    # Mount or COPY the directory you want serve into /var/www/site
#    docker-compose up

FROM debian:8
MAINTAINER John Andersen

RUN apt-get update -y && \
    apt-get install -y apache2 python && \
    apt-get clean && \
    rm -rf /var/cache/apt/* && \
    a2enmod cgi mod_python

COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
