#!/bin/sh

yum update -y
yum install -y glibc-langpack-en bzip2-devel wget curl vim make telnet python3

## Install Python libraries
echo $'\n\nInstall Python libraries'
pip3 install --upgrade pip
pip3 install gunicorn==19.9.0 requests==2.26.0 urllib3==1.26.5 cryptography==36.0.2 requests-oauthlib==1.1.0 pyOpenSSL==19.0.0 flask==1.1.1 Flask-OAuthlib==0.9.6 oauthlib==2.1.0 bcrypt==3.1.7 Jinja2==2.11.3 azure-data-tables==12.0.0b4

echo $'\n\nRemove temporary files'
rm -Rf Dockerfile createImage.sh requirements.sh .git
