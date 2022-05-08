#!/usr/bin/env bash

usage() {
  echo "Usage: bash_script.sh [OPTIONS] EXAMPLE_ARGUMENT

Options:
  --example-option VALUE       	Use this to pass an optional value
  --example-flag       		Use this as a flag
"
}

if [[ -z "$1" ]]; then
  usage && exit 1;
fi

example_argument="$1"

example_option="value"
example_flag="false"

. "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/parse_options.sh || exit 1;

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

