# VERSION:       0.1
# DESCRIPTION:   adb in a container
# AUTHOR:        John Andersen <johnandersenpdx@gmail.com>
# COMMENTS:
#   This file builds a container whose primary purpose is the
#   use of the android debugging bridge (adb)
# USAGE:
#   # Download adb Dockerfile
#	  wget http://raw.githubusercontent.com/
#
#	  # Build adb image
#	  docker build -t adb .
#
#   # Run adb container, privileged or you can map the usb volumes
#	  docker run --privileged --rm -ti adb

FROM debian:8
MAINTAINER John Andersen johnandersenpdx@gmail.com

# Install adb dependencies, adb needs 32-bit libs
RUN export DEBIAN_FRONTEND=noninteractive && \
    export SDK_VERSION="24.3.3" && \
    dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get -y install libc6:i386 libstdc++6:i386 wget unzip openjdk-7-jre-headless && \
    mkdir -pv ~/.android/ && \
    wget --progress=dot:giga -O /opt/adt.tgz \
      https://dl.google.com/android/android-sdk_r${SDK_VERSION}-linux.tgz && \
    tar xzf /opt/adt.tgz -C /opt && \
    rm /opt/adt.tgz && \
    echo y | /opt/android-sdk-linux/tools/android update sdk --filter platform-tools --no-ui --force && \
    rm -rf /opt/android-sdk-linux/tools/ && \
    apt-get -y purge wget unzip openjdk-7-jre-headless && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /usr/share/perl && \
    rm -rf /usr/share/man && \
    rm -rf /usr/share/locale && \
    rm -rf /usr/share/doc && \
    rm -rf /var/cache/apt/*

# Expose default adb port
EXPOSE 5037

# Set up PATH for adb
ENV PATH $PATH:/opt/android-sdk-linux/platform-tools:/opt/android-sdk-linux/tools

