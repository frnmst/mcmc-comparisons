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
    rm -rf *.csv
}

check_binaries()
{
    which ${BINARIES} || exit 1
} 1>/dev/null

list_available_experiment_names()
{
    printf "%s\n" "${LIST_OF_EXPERIMENT_NAMES}"
}

list_available_experiment_types()
{
    printf "%s\n" "${LIST_OF_EXPERIMENT_TYPES}"
}

plot_comparison()
{
    local experiment_name_a="${1}"
    local output_file_a="${2}"
    local first_experiment_only="${3}"
    local experiment_name_b="${4}"
    local output_file_b="${5}"

    [ -z "${experiment_name_b}" ] && unset experiment_name_b

    export MPLBACKEND=Agg
    python3 "${PLOT_DIRECTORY}"/plot_comparison.py \
        "${experiment_name_a}" \
        "${output_file_a}" \
        "${first_experiment_only}" \
        "${experiment_name_b}" \
        "${output_file_b}" \
        && printf "%s\n" 'check the resulting plots'
}

run_xsb_experiments()
{
    local experiment_name="${1}"
    local output_file="${2}"
    local min=${3}
    local max=${4}
    local step=${5}
    local run_label=${6}
    local resampling_style="${7}"
    local resampling_probability="${8}"
    local single_or_parallel="${9}"
    local startup_file_path=""${XSB_AMCMC_STARTUP_FILE}"_${run_label}.P"

    pushd "${XSB_AMCMC_DIRECTORY}"

    # Build the file.
    cat <<EOF > "${startup_file_path}"
:- go.
go :-
    consult('experiments.P'),
    experiments_${single_or_parallel}_${experiment_name}('${output_file}',${min},${max},${step},${run_label},'${resampling_style}',${resampling_probability}).

EOF

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

run_experiments_with_slurm()
{
    local experiment_name="${1}"
    local output_file="${2}"
    local min=${3}
    local max=${4}
    local step=${5}
    local memory_mb=${6}
    local partition="${7}"
    local slurm_conf_file='run_slurm.conf'
    local slurm_run_file='run_slurm.sh'
    local slurm_frontend_file='frontend.sh'

    cat <<EOF > "${slurm_conf_file}"
0-3 ./frontend.sh %t
EOF
    cat <<-EOF > "${slurm_frontend_file}"
#!/bin/bash
. ../includes/variables.sh
. ../includes/shared.sh
. ../includes/fbopt --no-remove-csv-files --experiment-name ${experiment_name} --min ${min} --max ${max} --step ${step} \\
EOF
    cat <<-"EOF" >> "${slurm_frontend_file}"
    --single-run-with-label=$((${1}+1)) --output-file="job-"${2}".csv"
EOF

    cat <<-EOF > "${slurm_run_file}"
#!/bin/bash
#SBATCH --partition=${partition}
#SBATCH --job-name=${experiment_name}
#SBATCH --ntasks=4 # cores
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=${memory_mb}
#SBATCH -o ${experiment_name}-%j.out # STDOUT
#SBATCH -e ${experiment_name}-%j.err # STDERR
EOF

    cat <<-"EOF" >> "${slurm_run_file}"

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

. ../includes/variables.sh
. ../includes/shared.sh

srun --multi-prog run_slurm.conf ${SLURM_JOB_ID}
EOF

chmod +x "${slurm_frontend_file}" "${slurm_run_file}"

# Since the slurm files source these scripts again it is better
# to start with a fresh environment.
#env --ignore-environment PATH="${HOME}:/usr/bin:." sbatch run_slurm.sh
sbatch run_slurm.sh
}
