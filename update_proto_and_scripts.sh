#!/bin/sh
cd ..
mkdir testnet
cd testnet
git clone https://github.com/libra/libra.git
cd libra
git checkout origin/testnet

rm ../../libra-client/proto/*.proto
find . -name *.proto | xargs cp -t ../../libra-client/proto/
cd ../../libra-client/
rpl "shared/mempool_status" "mempool_status" proto/mempool.proto

../../libra-client/transaction_scripts/gen_transaction_bytecode.sh
cp *.bytecode ../../libra-client/transaction_scripts/
#scp xn@an1:~/libra/

cd ../../libra-client/
./generate_protobuf.sh