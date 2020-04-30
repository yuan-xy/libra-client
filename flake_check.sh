#!/bin/bash
flake8 libra_client --count --select=E9,F --show-source --statistics
flake8 libra_client --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
