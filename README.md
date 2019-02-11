# mcmc-comparisons

comparision of various [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)

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
    - [CSV file format](#csv-file-format)
    - [Plot](#plot)
    - [Notes on running the tests](#notes-on-running-the-tests)
        - [Sequential version](#sequential-version)
        - [Output files](#output-files)
        - [An alternative to GNU Parallel](#an-alternative-to-gnu-parallel)
    - [References](#references)
        - [Algorithms](#algorithms)
        - [SLURM](#slurm)
            - [Configuration file](#configuration-file)
            - [Running](#running-1)
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
| [Matplotlib](https://matplotlib.org/) | <Python 3 library> | - | `3.0.2` |
| [NumPy](http://www.numpy.org/) | <Python 3 library> | - | `1.15.4` |
| [GNU Parallel](http://www.gnu.org/software/parallel/) | `/bin/parallel` | `$ parallel --version` | `parallel 20181222` |
| [cplint library](https://github.com/friguzzi/cplint) | - | - | `v4.5.0` |

## Installation

### Arch Linux based distros

    TODO

    # pacman -S git make tar curl    
    # pacman -S swi-prolog python3 python-matplotlib python-numpy parallel
    $ swipl
    ?- pack_install(cplint).
    $ mkdir --parents ~/build
    $ cd ~/build
    $ curl --output XSB.tar.gz http://xsb.sourceforge.net/downloads/XSB.tar.gz 
    $ tar -xvzf  XSB.tar.gz XSB
    $ cd XSB
    $ configure
    $ make

## Repository cloning

Since this repository contains submodules you need to clone it using the 
appropriate flag:

    $ git clone --recurse-submodules https://github.com/frnmst/mcmc-comparisons.git

## Running

### Help

```shell
Usage: run.sh [OPTIONS]
Run MCMC tests

Mandatory arguments to long options are mandatory for short options too.
Options:
    -f, --four-way-comparison           compare SWI and XSB experiments. In
                                        this case you need to specify the test
                                        names separating them with a colon
                                        character and specifing the SWI then
                                        XSB the test name, like this:
                                        'test_name_swi:test_name_xsb'
    -g, --graph                         run the plot script after the tests
    --graph-only                        run the plot script only
    -h, --help                          print this help
    --list-test-names                   list the available test
    --list-test-types                   list the available test types
    -m, --min=MIN                       starting number of samples
    --multi-switch                      enable multi switch instead of single
                                        switch for AMCMC XSB tests
    -M, --max=MAX                       ending number of samples
    -p, --parallel                      execute tests on separate computing
                                        threads. If this option is enabled the
                                        number of threads is determined by the
                                        '--threads' option. If this option is
                                        disabled, the runs are executed
                                        consecutively.
    --single-run-with-label=LABEL       run a single test with the specified
                                        run label. This option excludes
                                        both the '--parallel' option and the
                                        '--runs' option
    --print-flags                       print the enabled options. This can also
                                        be used to print the default options
    -r, --runs=RUNS, --threads=RUNS     the number of runs or computing threads.
                                        See the '--parallel' option for more
                                        information
    --no-remove-csv-files               avoid removing all csv files before
                                        running a test. This option defaults
                                        to false in all cases except when run
                                        with the '--graph-only' option. In that
                                        case the value of this option is
                                        fixed to true and cannot be changed.
                                        Set this option if you want to keep old
                                        results and appending new ones to the
                                        same file. Normally, you should not set
                                        this option
    -s, --steps=STEPS                   the number of samples between
                                        consecutive iterations
    -t, --test-name=NAME                the name of the test
    -y, --test-type=NAME                the type of the test

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

The purpose of using SLURM is to run the experiments is a multi node setup:

- Go to the slurm directory and run the shell file

      $ cd ./src/slurm && sbatch run_slurm.sh

- You may also run the test interactively

      $  cd ./src/slurm && ./run_slurm.sh

## CSV file format

The results of each test will be logged to a corresponding CSV file with the 
following line format, depending on the type of test:

    run_number,current_samples,mh_time,mh_probability,gibbs_time,gibbs_probability\n

or

    run_number,current_samples,adapt_on_time,adapt_on_probability,adapt_off_time,adapt_off_probability\n


where `\n` is the newline character (ASCII code 10).

`mh_time`,`gibbs_time`,`adapt_on_time`,`adapt_off_time` are computed in 
milliseconds.

## Plot

The tools necessary to plot the results are Python 3 and Matplotlib.

The plot script called `plot_comparison.py` can be found under the `./src/plot` 
directory:

1. it reads one or more CSV files written according to the CSV file 
   format rules in this readme. 
2. it plots the average running times of multiple runs for each 
   sample. The standard deviation of the running times for each sample is 
   plotted as error bars.

The same type of plot is done for the probabilities and has the purpose of 
determining the accuracy of the calculations.

## Notes on running the tests

### Sequential version

What follows id a pseudocode scheme for the sequential version

```
for j = 0, j < $runs, j++:
    for i = $min, i < $max, i += $step:
        samples = i
        time_mh = measure_mh(samples)
        time_gibbs = measure_gibbs(samples)
        print(samples, time_mh, time_gibbs)
```

### Output files

When running the tests in parallel the result of each iteration is written on 
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
    swipl -s tests ${2} ${3} ${4} ${i} 1 &
    job_id=("${job_id[@]}" $!)
done
wait ${job_id[@]}
```

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

#### Configuration file

A configuration file for SLURM is available at `./src/slurm/slurm.conf`. This 
is the configuration file I use for my setup.

#### Running

You can run the SLURM daemons by executing `./src/slurm/run_daemons.sh` as root.

## License

See the `LICENSE` file.
