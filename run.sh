#!/usr/bin/bash

swipl -s poc ${1} ${2} ${3}
if [ $? -ne 0 ]; then
    printf "%s\n" "help: "${0}" min max samples"
fi
