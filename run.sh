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

for output in $OUTPUTS; do
    rm -rf "${output}"
done

if [ "${1}" = "-p" ]; then
    # Parallel tests.
    if [ -z "${5}" ]; then
        printf "%s\n" "help: "${0}" -p min max samples runs"
        exit 1
    fi

    # Background processes.
    #
    # declare -a job_id
    # for i in $(seq 1 ${5}); do
    #    swipl -s tests ${2} ${3} ${4} ${i} 1 &
    #    job_id=("${job_id[@]}" $!)
    # done
    # wait ${job_id[@]}

    # GNU Parallel.
    seq 1 ${5} | parallel --lb swipl -s tests ${2} ${3} ${4} {} 1

else
    # Sequential tests.
    if [ -z "${4}" ]; then exit 1
        printf "%s\n" "help: "${0}" min max samples runs"
        exit 1
    fi
        swipl -s tests ${1} ${2} ${3} ${4} 0
fi

# FIXME: Move this stuff to python.
for output in $OUTPUTS; do
    # Sort lines by sample id and run number so that we maintain the correct
    # imput for the python script.
    cat "${output}" | tr ',' ' ' | sort -g -s -k 1 | tr ' ' ',' > "${output}".baak
    mv "${output}" "${output}".bak
    mv "${output}".baak "${output}"
done

MPLBACKEND=Agg ./plot_comparison.py

