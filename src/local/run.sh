#!/bin/bash
#
# run.sh
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Franco Masotti
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

OUTPUTS="arithm_sample.csv"
BINARIES="swipl parallel python3"
TESTS_DIRECTORY="../prolog"
PLOT_DIRECTORY="../plot"

help()
{
    printf "%s\n" "help: "${0}" -p min max samples runs"
    printf "%s\n" "      "${0}" min max samples runs"
}

for output in $OUTPUTS; do
    rm -rf "${output}"
done

which $BINARIES || exit 1
if [ -z "${1}" ]; then
    help
    exit 1
fi

if [ "${1}" = "-p" ]; then
    # Parallel tests.
    if [ -z "${5}" ]; then
        help
        exit 1
    fi
    # GNU Parallel.
    seq 1 ${5} | parallel --lb swipl -s "${TESTS_DIRECTORY}"/tests ${2} ${3} ${4} {} 1
else
    # Sequential tests.
    if [ -z "${4}" ]; then
        help
        exit 1
    fi
    swipl -s "${TESTS_DIRECTORY}"/tests ${1} ${2} ${3} ${4} 0
fi

# Plot.
export MPLBACKEND=Agg
python3 "${PLOT_DIRECTORY}"/plot_comparison.py
