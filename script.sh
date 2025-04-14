#! /bin/bash

if [ "$1" == "5" ]; then
    echo \"$1\"
    exit 0
else
    echo "PANIC: \"$1\""
    exit 1
fi
