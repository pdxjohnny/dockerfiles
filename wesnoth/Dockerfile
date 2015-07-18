# VERSION:                0.1
# DESCRIPTION:            Wesnoth game in a container
# AUTHOR:                 John Andersen <johnandersenpdx@gmail.com>
# COMMENTS:
#   This file builds a container which can be accessed via ssh
#   with username=user password=user over ssh to play wesnoth.
# USAGE:
#   # Download wesnoth Dockerfile
#   wget http://raw.githubusercontent.com/
#
#   # Build wesnoth image
#   docker build -t wesnoth .
#
#   # Run wesnoth container
#   docker run -d -P --name wesnoth-game wesnoth
#   docker port test 22
#       0.0.0.0:<port>
#   ssh -X -oStrictHostKeyChecking=no user@localhost -p <port> wesnoth-1.10 #password is user

FROM pdxjohnny/x11
MAINTAINER John Andersen

RUN apt-get update && \
    apt-get install -y wesnoth && \
    apt-get clean && \
    rm -rf /var/cache/apt/*

