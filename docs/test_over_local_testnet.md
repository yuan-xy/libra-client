## How to run `libra-client` commands and test cases over local libra-swarm

### Step 0: Prepare

Download `libra-client` and `libra` source code, ant put them in the same directory.

```sh
$ ls
libra-client libra
```

### Step 1: Start Local Libra testnet

cd the libra dir and start libra-swarm:

```sh
$ cd libra
$ cargo run -p libra-swarm
```

You will see something like this:

```plaintext
Faucet account created in (loaded from) file "/tmp/3b201f0f792e5736daa1b2330d72562b/temp_faucet_keys"
To run the Libra CLI client in a separate process and connect to the validator nodes you just spawned, use this command:
        cargo run --bin client -- -a localhost -p 52014 -s "./tmp1/0/consensus_peers.config.toml" -m "/tmp/3b201f0f792e5736daa1b2330d72562b/temp_faucet_keys"
```

of course, you can run `libra-client` by specify above parameters, for example:

```
libra -a localhost -p 52014 -s "./tmp1/0/consensus_peers.config.toml" -m "/tmp/3b201f0f792e5736daa1b2330d72562b/temp_faucet_keys"
```

but you can't run test over local libra-swarm. Below tests connect to libra testnet "ac.testnet.libra.org", not yours network.

```sh
$ cd libra-client
$ pytest test
```


### Step 2: Copy faucet file from libra to libra-client

This step can be omit in the past, but recent update of `libra` seems changes faucet file everytime and you cann't specify a faucet key before libra-swarm start.

```
cp /tmp/3b201f0f792e5736daa1b2330d72562b/temp_faucet_keys libra-client/libra/faucet_key_for_test
```

### Step 3: Export `TESTNET_LOCAL` to env

```
$ cd libra-client
$ export TESTNET_LOCAL="localhost;52014;../libra/tmp1/0/consensus_peers.config.toml"
```

Now you can run test over your local testnet.

```sh
$ pytest test
```

Because the test code assume there are at least 2 transaction in the blockchain, so your first test will fail on a fresh started libra-swarm. But you can run `pytest test` twice, and the second round will pass.


Also, you can run `libra` and `libra_shell` commands over your local libra-swarm without extra parameters.
