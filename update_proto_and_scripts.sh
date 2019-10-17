#!/bin/sh
cd ..
mkdir testnet
cd testnet
git clone https://github.com/libra/libra.git
cd libra
git checkout origin/testnet

cp ./scripts/cli/consensus_peers.config.toml ../../libra-client/libra

../../libra-client/transaction_scripts/gen_transaction_bytecode.sh
cp ./language/stdlib/transaction_scripts/*.mv ../../libra-client/transaction_scripts/
#scp xn@an1:~/libra/

rm ../../libra-client/proto/*.proto
find . -name *.proto | xargs cp -t ../../libra-client/proto/
cd ../../libra-client/
rpl "shared/mempool_status" "mempool_status" proto/mempool.proto


cd ../../libra-client/
./generate_protobuf.sh