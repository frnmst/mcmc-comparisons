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

OUTPUTS="arithm_sample.csv test33_sample.csv"
BINARIES="swipl parallel python3"
TESTS_DIRECTORY="../prolog"
PLOT_DIRECTORY="../plot"

help()
{
    printf "%s\n" "help: "${0}" -p -n test_name -s \"min max samples runs\""
}

remove_result_files()
{
    for output in $OUTPUTS; do
        rm -rf "${output}"
    done
}

check_binaries()
{
    which $BINARIES || exit 1
}

main()
{
    local argc="${1}"
    local getopt_options='n:phg'
    local getopt_long_options="min:,max:,step:,runs:,"
    local graph='false'
    local test_name=''
    local help='false'
    local parallel='false'

    check_binaries
    remove_result_files

    opts="$(getopt --options "${getopt_options}" --longoptions "${getopt_long_options}" -- ${argc})"
    eval set -- "$opts"

    while true; do
        case "${1}" in
            --min ) min="${2}";
                    shift 1 ;;
            --max ) max="${2}";
                    shift 1 ;;
            --step ) step="${2}";
                    shift 1 ;;
            --runs ) runs="${2}";
                    shift 1 ;;
            -g ) graph='true' ;;
            -h ) help='true' ;;
            -n ) test_name="${2}";
                 shift 1 ;;
            -p ) parallel='true' ;;
            -- ) break ;;
        esac
        shift 1
    done

    if [ "${help}" = 'true' ]; then
        help
        exit 0
    fi

    if [ -z "${test_name}" ] \
        || [ -z "${min}" ] \
        || [ -z "${max}" ] \
        || [ -z "${step}" ] \
        || [ -z "${runs}" ]; then
        help
        exit 1
    fi

    if [ "${parallel}" = 'true' ]; then
        seq 1 ${runs} | parallel --lb swipl -s "${TESTS_DIRECTORY}"/tests "${test_name}" ${min} ${max} ${step} {} 1
    else
        swipl -s "${TESTS_DIRECTORY}"/tests "${test_name}" ${min} ${max} ${step} ${runs} 0
    fi

    if [ "${graph}" = 'true' ]; then
        export MPLBACKEND=Agg
        python3 "${PLOT_DIRECTORY}"/plot_comparison.py
        printf "%s\n" "check the resulting plot"
    fi
}

main "$*"

