#!/bin/sh

mkdir ./ssl
cp /opt/wildfly/ssl/eyttda_com.crt ./ssl/intaxlligence-crt
cp /opt/wildfly/ssl/eyttda_com.key ./ssl/intaxlligence-key

sudo docker stop template_front
sudo docker rm template_front
sudo docker image rm template_front
sudo docker build . -t template_front
sudo docker run -d -p 54000:443/tcp --restart=always --add-host=pro.eyttda.com:172.17.0.1 -e TZ=America/Mexico_City  --name template_front template_front
sudo docker ps
rm -Rf ./ssl
