#!/bin/bash
#
# variables.sh
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

BINARIES='swipl xsb parallel python3 nice'
EXPERIMENTS_DIRECTORY='../prolog'
PLOT_DIRECTORY='../plot'
LIST_OF_EXPRIMENT_NAMES='arithm_sample arithm_sample_three arithm_rejection_sample test33_sample test66_sample test33_cond_prob arithm_cond_prob hmm_sample_three'
LIST_OF_EXPERIMENT_TYPES='swi xsb'
XSB_AMCMC_DIRECTORY='../prolog/amcmc/xsb'
# Relative to $XSB_AMCMC_DIRECTORY
XSB_AMCMC_STARTUP_FILE='startup_experiments.P'

# Assign default values for the flags.
MIN='1000'
MAX='10000'
STEP='1000'
RUNS='4'
EXPERIMENT_NAME='arithm_sample'
REPETITIONS=0
MEMORY=8192
PARTITION='normal'
# Empty means False.
FIRST_EXPERIMENT_ONLY=''
