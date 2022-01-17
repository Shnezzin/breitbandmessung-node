#!/bin/bash

if [ $# -eq 0 ]; then
       me=`basename "$0"`
  echo "help:"
  echo "$me debian|alpine" 
  echo "Use '$me debian' for amd64, arm64 or arm/v/7 build" 
  echo "Use '$me alpine' for amd64 or arm64 build" 
  exit 0
fi
if [ $1 == debian ]
  then
echo "debian"
  docker build -f Dockerfile.debian -t breitbandmessung .
elif [ $1 == alpine ]
  then
echo "alpine"
  docker build -f Dockerfile -t breitbandmessung .
else
       me=`basename "$0"`
  echo "help:"
  echo "$me debian|alpine" 
  echo "Use '$me debian' for amd64, arm64 or arm/v/7 build" 
  echo "Use '$me alpine' for amd64 or arm64 build" 
  exit 0
fi
chmod +x $PWD/*.sh
docker stop breitbandmessung >> /dev/null
docker rm breitbandmessung >> /dev/null
mkdir $PWD/config
mkdir $PWD/messprotokolle
chmod 777 $PWD/messprotokolle
docker create -v $PWD/config/:/usr/src/app/config:rw -v $PWD/messprotokolle:/export/ --name "breitbandmessung" breitbandmessung:latest 
docker start breitbandmessung
exit 0
