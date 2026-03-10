#!/usr/bin/env bash
if test "$#" != 1; then
    echo "$0 requires an argument."
    exit 1
fi
if test ! -f "$1"; then
    echo "file does not exist: $1"
    exit 1
fi
IFS=""
while read -r line; do
    # Skip comments
    if [ "${line:0:1}" == "#" ]; then
        continue
    fi
    if [ ${#line} -ge 72 ]; then
        echo "Commit messages are limited to 72 characters."
        echo "The following commit message has ${#line} characters."
        echo "${line}"
        exit 1
    fi
done <"${1}"
exit 0
