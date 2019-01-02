#!/bin/bash
#
# shared.sh
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

remove_csv_files()
{
    for output in ${OUTPUTS}; do
        rm -rf "${output}"
    done
}

check_binaries()
{
    which ${BINARIES} || exit 1
} 1>/dev/null

list_available_test_names()
{
    printf "%s\n" "${LIST_OF_TEST_NAMES}"
}

list_available_test_types()
{
    printf "%s\n" "${LIST_OF_TEST_TYPES}"
}

plot_comparison()
{
    local test_name="${1}"

    export MPLBACKEND=Agg
    python3 "${PLOT_DIRECTORY}"/plot_comparison.py ""${test_name}".csv" \
        && printf "%s\n" "check the resulting plots"
}

run_xsb_tests()
{
    local test_name="${1}"
    local min=${2}
    local max=${3}
    local step=${4}
    local run_label=${5}
    local adaptation="${6}"
    local resampling_style="${7}"
    local single_or_parallel="${8}"

    pushd "${XSB_AMCMC_DIRECTORY}"

    # Build the file.
    cat <<-EOF
:- go.
go :-
    consult('tests.P'),
    tests_"${single_or_parallel}"_"${test_name}"(${min},${max},${step},${run_label},${adaptation},${resampling_style}).
EOF > startup_experiments_TWO.P

    # Since we cannot use argc/argv we must read the arguments from a
    # test file, just like the author of amcmc.
    xsb -e "compile('startup_experiments.P'),halt."
    xsb startup_experiments
    popd
}

