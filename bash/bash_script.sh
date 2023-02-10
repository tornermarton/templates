#!/usr/bin/env bash

# TODO: update usage
usage() {
  echo "Usage: bash_script.sh [OPTIONS] EXAMPLE_ARGUMENT

Options:
  --example-option VALUE       	Use this to pass an optional value
  --example-flag       		      Use this as a flag
"
}

# TODO: change $1 to the number of arguments
if [[ -z "$1" ]]; then
  usage && exit 1;
fi

# TODO: update arguments
example_argument="$1"

# TODO: update options
example_option="value"
example_flag="false"

# TODO: if parse_options.sh not in the same directory than modify this
. "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/parse_options.sh || exit 1;

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# TODO: remove example flag check
if [[ "$example_flag" == "true" ]]; then
  echo "flag is set"
fi
