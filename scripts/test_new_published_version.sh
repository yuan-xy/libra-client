#!/bin/bash
VER=`scripts/parse_version.py`
mkdir -p ~/test
python3 -m venv ~/test/$VER
source ~/test/$VER/bin/activate
pip install --index-url https://pypi.org/project/ libra-client==$VER
libra ledger time
