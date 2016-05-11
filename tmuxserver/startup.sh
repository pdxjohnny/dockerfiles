#!/bin/bash

su - wemux /usr/local/bin/wemux start

/usr/sbin/sshd -D
