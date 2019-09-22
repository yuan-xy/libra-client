# LibraClient  [![Build Status](https://travis-ci.org/yuan-xy/libra-client.svg?branch=master)](https://travis-ci.org/yuan-xy/libra-client) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)


LibraClient is an unofficial client for [Libra blockchain](http://libra.org) written in python language. The Client allows you interact whith Libra Network easily. For Python programmers, you can also call the client side api to interact with Libra Network.


## Installation

Require python 3.6 or above installed.

```sh
$ pip install libra-client
```

## Usage

For programmers, please see [Client side Libra API for python programmer](https://github.com/yuan-xy/libra-client#client-side-libra-api-for-python-programmer).

### Start Libra Client and Connect to the Testnet

To connect to a validator node running on the Libra testnet, run the client as shown below.

```bash
./scripts/cli/start_cli_testnet.sh
```

Once the client connects to a node on the testnet, you will see the following output.  To quit the client at any time, use the `quit` command.


```
usage: <command> <args>

Use the following commands:

account | a
  Account operations
query | q
  Query operations
transfer | transferb | t | tb
  <sender_account_address>|<sender_account_ref_id> <receiver_account_address>|<receiver_account_ref_id> <number_of_coins> [gas_unit_price (default=0)] [max_gas_amount (default 100000)] Suffix 'b' is for blocking.
  Transfer coins from account to another.
help | h
  Prints this help
quit | q!
  Exit this client


Please, input commands:

libra%
```


Once your client is connected to the testnet, you can run CLI commands to create new accounts.  [This document will guide you through executing your first transaction on the Libra Blockchain.](/first_transaction.md). We will walk you through creating accounts for two users (let's call them Alice and Bob).


## Client side Libra API for python programmer


### Wallet

You can create a wallet using `WalletLibrary` class. A wallet is like your masterkey and you can create almost infinitely many Libra accounts from it. Note that LibraClient's mnemonic scheme is compatible with that of [Libra's CLI](https://github.com/libra/libra/tree/master/client/src), so you can import mnemonic between the two libraries.

```py
import libra

# Create a new random wallet
wallet = libra.WalletLibrary.new()

# Create a new wallet from mnemonic words
wallet = libra.WalletLibrary.new_from_mnemonic(mnemonic, child_count)

# Recover wallet from a offical Libra CLI backup file
wallet = libra.WalletLibrary.recover(filename)
```

### Account

An `Account` can be created by calling `new_account` function on a wallet, each Account has an integer index in wallet, start from zero. An `Account` contains its `address`, `public_key`, and `private_key`.

```py

print(wallet.child_count)
account1 = wallet.new_account()
print(wallet.child_count)
print(account1.address)
print(account1.public_key)
print(account1.private_key)

```

### Client

A `Client` must be created in order to send protobuf message to a Libra node. You can create a client with the following code.

```py
from libra import Client

client1 = Client("testnet")  # Default client connecting to the official testnet
client2 = LibraClient('localhost:8000')  # Client connecting to a local node
```

### Get Account Data of an Address

``` plaintext
# An account stores its data in a directory structure, for example:
#   <Alice>/balance:   10
#   <Alice>/a/b/mymap: {"Bob" => "abcd", "Carol" => "efgh"}
#   <Alice>/a/myint:   20
#   <Alice>/c/mylist:  [3, 5, 7, 9]
#
# If someone needs to query the map above and find out what value associated with "Bob" is,
# `address` will be set to Alice and `path` will be set to "/a/b/mymap/Bob".
#
# On the other hand, if you want to query only <Alice>/a/*, `address` will be set to Alice and
# `path` will be set to "/a" and use the `get_prefix()` method from statedb
```

#### Get Account State Blob of an Address
You can query an account's raw blob by using `get_account_blob` function on `Client`. The function returns a tuple of account state blob and latest ledger version. The blob is a binary LCS serialize format of account data. If an account has not been created yet (never received any funds), the blob will be empty.

```py
client = Client("testnet")
blob, version = client.get_account_blob(address)
```
#### Get Account State Map data of an Address
If the Account has been created, you can call `get_account_state` function which return a map of path to data; other wise, AccountError will be thrown.

```py
client = Client("testnet")
amap = client.get_account_state(address)
```

#### Get Account Resource of an Address
If you want to get account balance / sequence / authentication_key etc from account state, you can calling `get_account_resource` function, which will deserialize the account resource from account state map.

```py
client = Client("testnet")
resource = client.get_account_resource(address)
print(resource.sequence_number)
print(resource.balance)
print(resource.authentication_key)
```

#### Get Balance of an Address
If you just want to get the balance of an address, simply call `get_balance` function.

```py
client = Client("testnet")
balance = client.get_balance(address)
```

#### Get Sequence Number of an Address

If you just want to get the sequence number of an address, simply call `get_sequence_number` function.

```py
client = Client("testnet")
balance = client.get_sequence_number(address)
```

### Mint Testnet Libra Token

You can mint testnet libra with `mint_with_faucet` function, which sends a HTTP POST request to [http://faucet.testnet.libra.org](http://faucet.testnet.libra.org).

```py
c = libra.Client("testnet")
c.mint_coins_with_faucet_service(address, 12345, is_blocking=True)
```

### Creating a Transfer Transaction Script and Sending the Transaction

Note that in the official testnet, the Libra node ONLY allows sending [the official transfer transaction script](https://github.com/libra/libra/blob/master/language/stdlib/transaction_scripts/peer_to_peer_transfer.mvir). In the future, this libra can be extended to support more transaction scripts as well!

```py
wallet = libra.WalletLibrary.recover('test.wallet')
a0 = wallet.accounts[0]
a1 = wallet.accounts[1]
ret = c.transfer_coin(a0, a1.address, 1234, is_blocking=True)
print(ret.ac_status.code)
```
When is_blocking param is False, the call will return as the transaction is submit to the validator node. When is_blocking param is True, the call will not return until the tranfer is actually executed or transaction waiting timeout.

### Query Events
TODO.