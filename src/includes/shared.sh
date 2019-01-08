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
    local resampling_style="${6}"
    local single_or_parallel="${7}"
    local startup_file_path=""${XSB_AMCMC_STARTUP_FILE}"_${run_label}.P"

    pushd "${XSB_AMCMC_DIRECTORY}"

    # Build the file.
    if [ ! -f "${startup_file_path}" ]; then
        cat <<EOF > "${startup_file_path}"

:- go.
go :-
    consult('tests.P'),
    tests_${single_or_parallel}_${test_name}(${min},${max},${step},${run_label},'${resampling_style}').

EOF
    fi

# For some reason I get the following if I don't add the sleep command.
#
#[xsb_configuration loaded]
#[sysinitrc loaded]
#[xsbbrat loaded]
#++Error[XSB/Runtime/P]: [Type (94589064825984 in place of atom)] in arg 1 of
#predicate atom_codes/2
#Forward Continuation...
#... string:atom_to_term/2  From /home/vm/build/XSB/syslib/string.xwam
#... string:atom_to_term/2  From /home/vm/build/XSB/syslib/string.xwam
#... loader:check_times_and_load/5  From /home/vm/build/XSB/syslib/loader.xwam
#... standard:call/1  From /home/vm/build/XSB/syslib/standard.xwam
#... standard:catch/3  From /home/vm/build/XSB/syslib/standard.xwam
#
#End XSB (cputime 0.01 secs, elapsetime 0.02 secs)
    sync &
    sleep 1
    wait $!

    # Since we cannot use argc/argv we must read the arguments from a
    # test file, just like the author of amcmc.
    xsb -e "compile('"${startup_file_path}"'),halt."
    xsb "${startup_file_path%.P}"
    rm "${startup_file_path}"
    popd
}
