#!/bin/sh
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
apt-get install -y nodejs npm
npm install -g htmlhint
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
