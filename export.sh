#!/usr/bin/env bash

./build.sh

docker save algorithm | gzip -c > algorithm.tar.gz
