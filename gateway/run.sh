#!/bin/bash

# IOTA address to send data/tx to. Just for demo purposes.
ADR=DCDZNWWCQC9NVUQCLPSOOQDPFBDTBDDGVPYSMG9QZTHRELVYJFOUQTONYMUKZTEUKHFQKJHNEHBHODZIW

docker kill iotademo
docker rm iotademo

docker run \
  --name iotademo \
  -d \
  --env IOTAADDRESS=${ADR} \
  -p 3000:3000 \
  iotademo:latest 

docker logs -f iotademo

