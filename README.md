# mcmc-comparisons

comparision of various [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) algorithms

## Table of contents

[](TOC)

- [mcmc-comparisons](#mcmc-comparisons)
  - [Table of contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Dependencies for the installation phase](#dependencies-for-the-installation-phase)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [Arch Linux based distros](#arch-linux-based-distros)
  - [Repository cloning](#repository-cloning)
  - [Running](#running)
    - [Help](#help)
    - [Run locally](#run-locally)
    - [Run on a SLURM queue](#run-on-a-slurm-queue)
      - [Plot](#plot)
      - [Configuration file](#configuration-file)
    - [CSV file format](#csv-file-format)
    - [Plot](#plot-1)
    - [Notes on running the experiments](#notes-on-running-the-experiments)
      - [Sequential version](#sequential-version)
      - [Output files](#output-files)
      - [An alternative to GNU Parallel](#an-alternative-to-gnu-parallel)
      - [The hmm experiment](#the-hmm-experiment)
    - [References](#references)
      - [Algorithms](#algorithms)
      - [SLURM](#slurm)
    - [License](#license)

[](TOC)

## Purpose

Compare different kinds of MCMC and AMCMC sampling algorithms to find out which
ones are faster.

## Dependencies for the installation phase

The following packages are needed only during the installation phase. You may 
remove them after the installation if not needed.

| Package | Executable | Version command | Package version |
|---------|------------|-----------------|-----------------|
| [git](https://git-scm.com/) | `/bin/git` | `$ git --version` | `git version 2.20.1` |
| [GCC, the GNU Compiler Collection](http://gcc.gnu.org) | `/bin/gcc` | `$ gcc --vserion` | `gcc (GCC) 8.2.1 20181127` |
| [GNU Make](http://www.gnu.org/software/make) | `/bin/make` | `$ make --version` | `GNU Make 4.2.1` |
| [GNU Tar](https://www.gnu.org/software/tar/) | `/bin/tar` | `$ tar --version` | `tar (GNU tar) 1.30` |
| [curl](https://curl.haxx.se) | `/bin/curl` | `$ curl --version` | `curl 7.63.0 (x86_64-pc-linux-gnu) libcurl/7.63.0 OpenSSL/1.1.1a zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.4) libssh2/1.8.0 nghttp2/1.35.1` |

## Dependencies

You need to install the following packages and the ones listed for
[fbopt](https://github.com/frnmst/fbopt#dependencies):

| Package | Executable | Version command | Package version |
|---------|------------|-----------------|-----------------|
| [SWI prolog](http://www.swi-prolog.org/) | `/bin/swipl` | `$ swipl --version` | `SWI-Prolog version 7.7.19 for x86_64-linux` |
| [XSB Prolog](https://www.xsb.com/what-we-do/emerging-technologies/xsb-prolog.html) | \<Depends on installation> | `$ xsb --version` | `XSB Version 3.8.0 (Three-Buck Chuck) of October 28, 2017` |
| [Python 3](http://www.python.org/) | `/bin/python3` | `$ python3 --version` | `Python 3.7.1` | 
| [Matplotlib](https://matplotlib.org/) | \<Python 3 library> | - | `3.0.2` |
| [NumPy](http://www.numpy.org/) | \<Python 3 library> | - | `1.15.4` |
| [GNU Parallel](http://www.gnu.org/software/parallel/) | `/bin/parallel` | `$ parallel --version` | `parallel 20181222` |
| [cplint](https://github.com/friguzzi/cplint) | \<SWI Prolog library> | - | `v4.5.0` |

## Installation

### Arch Linux based distros

    # pacman -S git gcc make tar curl
    # pacman -S swi-prolog python3 python-matplotlib python-numpy parallel
    $ swipl
    ?- pack_install(cplint).
    $ mkdir --parents ~/build
    $ cd ~/build
    $ curl --output XSB.tar.gz http://xsb.sourceforge.net/downloads/XSB.tar.gz 
    $ tar -xvzf XSB.tar.gz
    $ cd XSB/build
    $ ./configure
    $ ./makexsb
    $ cd ~
    $ echo "alias xsb=\"~/build/XSB/bin/xsb\"" >> ~/.bashrc

## Repository cloning

Since this repository contains submodules you need to clone it using the 
appropriate flag:

    $ git clone --recurse-submodules https://github.com/frnmst/mcmc-comparisons.git

## Running

### Help

```shell
Usage: run.sh [OPTIONS]
Run MCMC experiments

Mandatory arguments to long options are mandatory for short options too.
Options:
    --first-experiment-only             keep the first experiment and discard all
                                        the others while plotting. The CSV file
                                        will remain unaltered
    -g, --graph                         run the plot script after the experiments
    --graph-only                        run the plot script only
    -h, --help                          print this help
    --list-experiment-names             list the available experiment
    --list-experiment-types             list the available experiment types
    -m, --min=MIN                       starting number of samples
    --multi-switch=RESAMPLINGPROB       enable multi switch instead of single
                                        switch for AMCMC XSB experiments with the
                                        specified resampling probability. This
                                        number goes from 0.0 to 1.0
    -M, --max=MAX                       ending number of samples
    -p, --parallel                      execute experiments on separate computing
                                        threads. If this option is enabled the
                                        number of threads is determined by the
                                        '--threads' option. If this option is
                                        disabled, the runs are executed
                                        consecutively
    --single-run-with-label=LABEL       run a single experiment with the specified
                                        run label. This option excludes
                                        both the '--parallel' option and the
                                        '--runs' option
    --print-flags                       print the enabled options. This can also
                                        be used to print the default options
    -r, --runs=RUNS, --threads=RUNS     the number of runs or computing threads.
                                        See the '--parallel' option for more
                                        information
    --memory=MEMORYMB                   the amount om memory in MB assigned
                                        to the SLURM job
    --no-remove-csv-files               avoid removing all csv files before
                                        running a experiment. This option defaults
                                        to false in all cases except when run
                                        with the '--graph-only' option. In that
                                        case the value of this option is
                                        fixed to true and cannot be changed.
                                        Set this option if you want to keep old
                                        results and appending new ones to the
                                        same file. Normally, you should not set
                                        this option
    --output-file                       use custom output filename.
                                        Defaults to ""${experiment_name}".csv"
                                        where "${experiment_name}" is given
                                        by the '--experiment-name' option
    --partition=PARTITIONNAME           the partition name used for the
                                        SLURM job
    -s, --steps=STEPS                   the number of samples between
                                        consecutive iterations
    --swi-vs-xsb                        compare SWI and XSB experiments. In
                                        this case you need to specify the experiment
                                        names separating them with a colon
                                        character and specifing the SWI then
                                        XSB the experiment name, as the argument
                                        of the '--experiment-name' option:
                                        'experiment_name_swi:experiment_name_xsb'
    -S, --slurm                         run the experiments with the SLURM system.
                                        This disables the '--graph', '--parallel'
                                        options and implies the
                                        '--single-run-with-label' option
    -t, --experiment-name=NAME          the name of the experiment
    -y, --experiment-type=NAME          the type of the experiment

Exit status:
 0  if OK,
 1  if an error occurred.

This software is released under the BSD 2-Clause license
Copyright (c) 2018-2019, Franco Masotti
```

### Run locally

- Go to the local directory

      $ cd ./src/local

- Execute the `run.sh` script, for example like this:

      $ ./run.sh -p -g

### Run on a SLURM queue

The purpose of using SLURM is to run the experiments is a multi node setup.

Before continuing you must start the daemons

    $ cd ./includes
    # ./run_slurm_daemons.sh

To run an experiment you must simply use the slurm option, like this

    $  ./run.sh -S

#### Plot

The plot needs to be rendered manually like this

    $ ./run.sh --graph-only -t "${experiment_name}"

#### Configuration file

A configuration file for SLURM is available at `./src/includes/slurm.conf`. This 
is the configuration file I use for my setup.

*Note: enforcement of memory limits is disabled in the provided 
configuration file. See also the `--mem` option at 
https://slurm.schedmd.com/sbatch.html*

## CSV file format

The results of each test will be logged to a corresponding CSV file with the 
following line format, depending on the type of experiment:

    run_number,current_samples,mh_time,mh_probability,gibbs_time,gibbs_probability\n

or

    run_number,current_samples,adapt_on_time,adapt_on_probability,adapt_off_time,adapt_off_probability\n

or

    run_number,current_samples,mh_time,mh_probability,gibbs_time,gibbs_probability,rejection_time,rejection_probability\n

where `\n` is the newline character (ASCII code 10).

`mh_time`,`gibbs_time`,`adapt_on_time`,`adapt_off_time` are computed in 
milliseconds.

## Plot

The tools necessary to plot the results are Python 3 and Matplotlib.

The plot script called `plot_comparison.py` can be found under the `./src/plot` 
directory and it plots:

1. the running time over samples
2. the probability over samples, to determine the accuracy of the calculations
3. the probability over running time, to determine convergence

Normally, the average of multiple runs is done for plots 1 and 2. The error bars
represent the standard deviation of the values. It is also possible to ignore
the average and consider only the first run via the `--first-experiment-only`
option.

## Notes on running the experiments

### Sequential version

What follows is a pseudocode scheme for the sequential version of one of the
experiments

```
for j = 0, j < $runs, j++:
    for i = $min, i < $max, i += $step:
        samples = i
        time_mh = measure_mh(samples)
        time_gibbs = measure_gibbs(samples)
        print(samples, time_mh, time_gibbs)
```

### Output files

When running the experiments in parallel the result of each iteration is written on 
the same output file thus producing an unsorted output. To fix this you may run
the following shell commands

```shell
for output in $OUTPUTS; do
    # Sort lines by run number and and keep sample id in place so that we maintain the correct
    # input for the python script.
    cat "${output}" | tr ',' ' ' | sort -g -s -k 1 | tr ' ' ',' > "${output}".baak
    mv "${output}" "${output}".bak
    mv "${output}".baak "${output}"
done
```

`plot_comparison.py` however sorts the data internally so if you use that 
script there is not need to fix the file by hand.

### An alternative to GNU Parallel

Use background processes:

```shell
declare -a job_id
for i in $(seq 1 ${5}); do
    swipl -s experiments ${2} ${3} ${4} ${i} 1 &
    job_id=("${job_id[@]}" $!)
done
wait ${job_id[@]}
```

### The hmm experiment

Before running this experiment you need to patch the file with git:

    $ pushd ./src/prolog && git -C swish/ am --signoff ../fix_hmm.patch && popd

This patch has been optained using a modified version of `hmm.pl` and this command:

    $ git format-patch HEAD~1..HEAD  --stdout > fix_hmm.patch

## References

### Algorithms

- [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm)
- [Gibbs sampling](https://en.wikipedia.org/wiki/Gibbs_sampling)
- [Adaptive MCMC](http://arxiv.org/abs/1403.6036)
  - [git repository](https://github.com/arunwise/Adaptive-MCMC)

### SLURM

- [SLURM](https://slurm.schedmd.com/)
- [SLURM serial jobs](https://www.chpc.utah.edu/documentation/software/serial-jobs.php)
- [SLURM Multi Program Usage](https://www.tchpc.tcd.ie/node/167)
- [SLURM configurator tool](https://slurm.schedmd.com/configurator.html)
- [The Slurm job scheduler](http://www.arc.ox.ac.uk/content/slurm-job-scheduler)
- [Slurm - Arch Wiki](https://wiki.archlinux.org/index.php/Slurm)

## License

See the `LICENSE` file.
