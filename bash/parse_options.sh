#!/usr/bin/env bash

# Copyright 2012  Johns Hopkins University (Author: Daniel Povey);
#                 Arnab Ghoshal, Karel Vesely

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# See the Apache 2 License for the specific language governing permissions and
# limitations under the License.


# Parse command-line options.
# To be sourced by another script (as in ". parse_options.sh").
# Option format is: --option-option_name arg
# and shell variable "option_name" gets set to value "arg".
# The exception is --help, which takes no arguments, but prints the
# $usage variable (if defined).

while true; do
  [[ -z "${1:-}" ]] && break;  # break if there are no arguments (left)

  case "$1" in
    # If the enclosing script is called with --help option, print the help
    # message and exit.  Scripts should put help messages in $usage
    --help|-h)
      if [[ "$(type -t usage)" == 'function' ]]; then
        usage
      else
        echo "No help found." 1>&2
      fi

      exit 0
      ;;
    --*=*)
      echo "$0: options to scripts must be of the form --option_name value, got '$1'"
      exit 1
      ;;
    # If the first command-line argument begins with "--" (e.g. --foo-bar),
    # then work out the variable option_name as $option_name, which will equal "foo_bar".
    --*)
      option_name=$(echo "$1" | sed s/^--// | sed s/-/_/g);
      # Next we test whether the variable in question is undefined-- if so it's
      # an invalid option and we die.  Note: $0 evaluates to the option_name of the
      # enclosing script.
      # The test [ -z ${foo_bar+xxx} ] will return true if the variable foo_bar
      # is undefined.  We then have to wrap this test inside "eval" because
      # foo_bar is itself inside a variable ($option_name).
      eval '[[ -z "${'$option_name'+xxx}" ]]' && echo "$0: invalid option $1" 1>&2 && exit 1;

      oldval="`eval echo \\$$option_name`";

      # Work out whether we seem to be expecting a Boolean argument.
      if [[ "$oldval" == "true" ]] || [[ "$oldval" == "false" ]]; then
	     was_bool=true;
      else
	     was_bool=false;
      fi

      # Set the variable to the right value-- the escaped quotes make it work if
      # the option had spaces, like --cmd "queue.pl -sync y"
      eval $option_name=\"$2\";

      # Check that Boolean-valued arguments are really Boolean.
      if ${was_bool}; then
        if [[ "$oldval" == "true" ]]; then
          eval $option_name=\"false\";
        else
          eval $option_name=\"true\";
        fi

        shift 1;
      else
        eval $option_name=\"$2\";
        shift 2;
      fi
      ;;
    *)
      # Skip arguments
      shift 1;
      ;;
  esac
done

true; # so this script returns exit code 0.
