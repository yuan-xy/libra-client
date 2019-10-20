#!/bin/bash

libra='python3 libra/cli/main.py -c always'

rm "docs/cli_help.html"
touch "docs/cli_help.html"
echo "<html><body>" >> "docs/cli_help.html"

echo "The command 'libra' contains four subcommands 'account', 'transaction', 'wallet', 'ledger'.
When you enter 'libra' without any other parameters and subcommands, the help information below is displayed.<br/><br/>"  >> "docs/cli_help.html"

gen_cmd_help () {
   echo "%libra $1" >> "docs/cli_help.html"
   echo "<hr/><pre>" >> "docs/cli_help.html"
   $libra $1 | ansi2html -i >> "docs/cli_help.html"
   echo "</pre></hr>" >> "docs/cli_help.html"
   #
}


gen_cmd_help ""

gen_cmd_help "account"

gen_cmd_help "transaction"

gen_cmd_help "wallet"

gen_cmd_help "ledger"

echo "</body></html>" >> "docs/cli_help.html"

