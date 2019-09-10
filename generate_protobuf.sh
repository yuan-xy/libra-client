#!/bin/sh

python3 -m grpc_tools.protoc \
    -I proto \
    --python_out=libra/proto \
    --grpc_python_out=libra/proto \
    proto/*.proto
