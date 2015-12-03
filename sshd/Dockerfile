# VERSION:                0.1
# DESCRIPTION:            X11 and Openssh server in a container
# AUTHOR:                 John Andersen <johnandersenpdx@gmail.com>
# COMMENTS:
#   This file builds a container which can be accessed via ssh
#   with username=user password=user. Usefull as a base image
#   for a conatiner which whishes to install gui software
# USAGE:
#    # Download x11 Dockerfile
#    wget http://raw.githubusercontent.com/
#
#    # Build x11 image
#    docker build -t x11 .
#
#   # Run x11 container
#   docker run -d -P --name test x11
#   docker port test 22
#   ssh -X -oStrictHostKeyChecking=no user@localhost -p 32771 xeyes #password is user

FROM ubuntu:14.04
MAINTAINER John Andersen

RUN apt-get update -y && \
    apt-get install -qqy openssh-server && \
    apt-get clean && \
    rm -rf /var/cache/apt/* && \
    mkdir /var/run/sshd && \
    /usr/sbin/useradd user && \
    echo "user:user" | chpasswd && \
    mkdir home/user && \
    chown user:user /home/user/

CMD    ["/usr/sbin/sshd", "-D"]

