# LibraClient  [![Build Status](https://travis-ci.org/yuan-xy/libra-client.svg?branch=master)](https://travis-ci.org/yuan-xy/libra-client) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)


LibraClient is a collection of tools which allows you interact whith [Libra Network](http://libra.org) easily. It contains three tools that provide three ways to access Libra:

1. `libra_shell`, an interactive shell program. It is compatible with official Libra client. For beginners, it lets you get started directly to try your first transaction with libra without requiring time-consuming downloads and compiles the huge entire Libra project source code.
2. `libra`, a command line tool. It has a modern colorful text interface and its output is the standard json format. So, it can be integrated to any programming language easily.
3. `python api`, a collection of apis for client access to libra. For Python programmers, you can call this client side api to interact with Libra Network with more control than by using `libra` command.

## Installation

Require python 3.6 or above installed.

```sh
$ python3 -m pip install libra-client
```

## Usage

### Start Libra Shell and Connect to the Testnet

To connect to a validator node running on the Libra testnet, run the client as shown below.

```bash
$ libra_shell
```

Once the client connects to a node on the testnet, you will see the following output.  To quit the client at any time, use the `quit` command.

![libra shell](https://github.com/yuan-xy/libra-client/raw/master/docs/shell.jpg "libra shell")



[This document will guide you through executing your first transaction on the Libra Blockchain.](/first_transaction.md). We will walk you through creating accounts for two users (let's call them Alice and Bob).


### Usage of Libra Command


```bash
$ libra
```

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
client2 = Client.new('localhost', 8000, "validator_file_path")  # Client connecting to a local node
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


### Query Transactions

Get transaction by version:

```py
c = libra.Client("testnet")
signed_txn = c.get_transaction(1)
print(signed_txn.raw_txn)
```
above code get transaction no.1, the return type is a SignedTransaction.

```py
class SignedTransaction(Struct):
    _fields = [
        ('raw_txn', RawTransaction),
        ('public_key', [Uint8, ED25519_PUBLIC_KEY_LENGTH]),
        ('signature', [Uint8, ED25519_SIGNATURE_LENGTH])
    ]
```

To get a list of transactions:

```py
c = libra.Client("testnet")
c.get_transactions(start_version, limit)
```

### Query Events
To get the latest 2 events send by an address:

```py
c = libra.Client("testnet")
events = c.get_latest_events_sent(address, 2)
```

To get the latest 2 events received by an address:

```py
c = libra.Client("testnet")
events = c.get_latest_events_received(address, 2)
```

Query events sent from an address, start from start_sequence_number(count begin with 0), get limit number of events, direction is ascending/descending:

```py
get_events_sent(self, address, start_sequence_number, ascending=True, limit=1)
```

Query events received from an address, start from start_sequence_number(count begin with 0), get limit number of events, direction is ascending/descending:

```py
get_events_received(self, address, start_sequence_number, ascending=True, limit=1)
```

