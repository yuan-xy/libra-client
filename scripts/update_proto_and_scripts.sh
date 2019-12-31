#!/bin/sh
cd ..
mkdir testnet
cd testnet
git clone https://github.com/libra/libra.git
cd libra
git checkout origin/testnet


#scp xn@an1:~/libra/

rm ../../libra-client/proto/*.proto
find . -name *.proto | xargs cp -t ../../libra-client/proto/
#rpl "shared/mempool_status" "mempool_status" proto/mempool.proto


cd ../../libra-client/
./scripts/generate_protobuf.sh