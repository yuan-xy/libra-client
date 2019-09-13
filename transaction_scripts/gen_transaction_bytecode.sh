cargo run -p compiler -- -o mint.bytecode ./language/stdlib/transaction_scripts/mint.mvir
cargo run -p compiler -- -o peer_to_peer_transfer.bytecode ./language/stdlib/transaction_scripts/peer_to_peer_transfer.mvir
cargo run -p compiler -- -o rotate_authentication_key.bytecode ./language/stdlib/transaction_scripts/rotate_authentication_key.mvir
cargo run -p compiler -- -o create_account.bytecode ./language/stdlib/transaction_scripts/create_account.mvir