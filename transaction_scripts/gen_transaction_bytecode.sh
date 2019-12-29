cd ../libra/
cargo run -p compiler --  ./language/stdlib/transaction_scripts/add_validator.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/remove_validator.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/register_validator.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/peer_to_peer_transfer.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/peer_to_peer_transfer_with_metadata.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/create_account.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/mint.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/rotate_authentication_key.mvir
cargo run -p compiler --  ./language/stdlib/transaction_scripts/rotate_consensus_pubkey.mvir

mv  ./language/stdlib/transaction_scripts/add_validator.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/remove_validator.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/register_validator.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/peer_to_peer_transfer.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/peer_to_peer_transfer_with_metadata.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/create_account.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/mint.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/rotate_authentication_key.mv ../libra-client/transaction_scripts/
mv  ./language/stdlib/transaction_scripts/rotate_consensus_pubkey.mv ../libra-client/transaction_scripts/
