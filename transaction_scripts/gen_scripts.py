import os, json

whitelists = [
    "add_validator",
    "remove_validator",
    "register_validator",
    "peer_to_peer_transfer",
    "peer_to_peer_transfer_with_metadata",
    "create_account",
    "mint",
    "rotate_authentication_key",
    "rotate_consensus_pubkey",
]

def compile(script):
    cmds = [
        "cd ../libra",
        f"cargo run -p compiler --  ./language/stdlib/transaction_scripts/{script}.mvir",
        f"mv ./language/stdlib/transaction_scripts/{script}.mv ../libra-client/transaction_scripts/"
    ]
    cmd = " && ".join(cmds)
    print(cmd)
    os.system(cmd)


# for script in whitelists:
#     compile(script)

def get_code_by_filename(script_file):
    with open(script_file) as f:
        amap = json.load(f)
        return amap['code']

bytecodes = {}

for script in whitelists:
    code = get_code_by_filename(f"transaction_scripts/{script}.mv")
    bytecodes[script] = code
    print(f"'{script}' : {code},\n")

#print(json.dumps(bytecodes))