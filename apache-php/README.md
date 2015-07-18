# apache-php

Setup
---
Download Dockerfile
Add what ever you need ( php addons like mysql mongo ) to apt-get install line

Build
---
docker build -t apache-php .
mkdir www
mkdir sites-enabled

Run
---
docker run --name test-apache-php -p 80:80 -v ${PWD}/www:/var/www -v ${PWD}/sites-enabled:/etc/apache2/sites-enabled -d apache-php


