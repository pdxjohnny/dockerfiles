# VERSION:       0.1
# DESCRIPTION:   ircd in a container
# AUTHOR:        John Andersen <johnandersenpdx@gmail.com>
# COMMENTS:
#   This file builds a container whose primary purpose is the
#   use of the android debugging bridge (ircd)
# USAGE:
#   # Download ircd Dockerfile
#	  wget http://raw.githubusercontent.com/
#
#	  # Build ircd image
#	  docker build -t ircd .
#
#   # Run ircd container
#	  docker run --rm -ti -p 6667:6667 ircd

FROM debian:8
MAINTAINER John Andersen johnandersenpdx@gmail.com

# Install ircd
RUN export DEBIAN_FRONTEND=noninteractive && \
    export PROXY_PORT="911" && \
    export PROXY_HOST="10.7.211.16" && \
    export no_proxy=".intel.com,10.23.232.47" && \
    export NO_PROXY=".intel.com,10.23.232.47" && \
    export http_proxy="http://${PROXY_HOST}:${PROXY_PORT}" && \
    export HTTP_PROXY="http://${PROXY_HOST}:${PROXY_PORT}" && \
    export https_proxy="http://${PROXY_HOST}:${PROXY_PORT}" && \
    export HTTPS_PROXY="http://${PROXY_HOST}:${PROXY_PORT}" && \
    apt-get update && \
    apt-get -y install ircd-irc2 && \
    apt-get clean && \
    rm -rf /var/cache/apt/* && \
    echo -e "\nno_oper_flood = yes;\ntrue_no_oper_flood = yes;\n" >> /etc/ircd/ircd.conf && \
    echo -e "auth {\n    user = "*@*";\n    class = "users";\n    #restricted = yes;\n    have_ident = no;\n    can_flood = yes;\n    };\n" >> /etc/ircd/ircd.conf && \
    sed -i "s/irc.localhost/localhost/g" /etc/ircd/ircd.conf

CMD ["/usr/sbin/ircd"]
