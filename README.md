# mcmc-comparisons

comparision of various [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)

## Table of contents

[](TOC)

- [mcmc-comparisons](#mcmc-comparisons)
    - [Table of contents](#table-of-contents)
    - [Purpose](#purpose)
    - [Installation](#installation)
    - [Running](#running)
        - [Run locally](#run-locally)
            - [Help](#help)
            - [Sequential version](#sequential-version)
        - [Run on a SLURM queue](#run-on-a-slurm-queue)
    - [CSV file format](#csv-file-format)
        - [Rules](#rules)
    - [Plot](#plot)
    - [Notes on running the tests in parallel](#notes-on-running-the-tests-in-parallel)
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

## Installation

- Install the latest version of [SWI prolog](http://www.swi-prolog.org/).
- Install the [Cplint library](https://github.com/friguzzi/cplint) and all the 
  suggested dependencies.

      $ swipl

      Welcome to SWI-Prolog (threaded, 64 bits, version 7.7.19)
      SWI-Prolog comes with ABSOLUTELY NO WARRANTY. This is free software.
      Please run ?- license. for legal details.

      For online help and background, visit http://www.swi-prolog.org
      For built-in help, use ?- help(Topic). or ?- apropos(Word).

      ?- pack_install(cplint).

- Install the latest version of 
  [XSB Prolog](https://www.xsb.com/what-we-do/emerging-technologies/xsb-prolog.html)

- Install [Python 3](http://www.python.org/), 
  [Matplotlib](https://matplotlib.org/),
  [NumPy](http://www.numpy.org/),
  [GNU Parallel](http://www.gnu.org/software/parallel/)
  [GNU Bash](http://www.gnu.org/software/bash/bash.html)
  [util-linux](https://www.kernel.org/pub/linux/utils/util-linux/)

- Clone the repository with the swish git submodule:

      $ git clone --recurse-submodules https://github.com/frnmst/mcmc-comparisons.git

## Running

### Run locally

- Go to the local directory

      $ cd src/local

- Execute the `run.sh` script, for example like this:

      $ ./run.sh -p -g


#### Help

```shell
FIXME
```

#### Sequential version

What follows id a pseudocode scheme for the sequential version

```
for j = 0, j < $runs, j++:
    for i = $min, i < $max, i += $step:
        samples = i
        time_mh = measure_mh(samples)
        time_gibbs = measure_gibbs(samples)
        print(samples, time_mh, time_gibbs)
```

### Run on a SLURM queue

The purpose of using SLURM is to run the tests in parallel.

- Go to the slurm directory and run the shell file

      $ cd src/slurm && sbatch run_slurm.sh

- You may also run the test interactively

      $  cd src/slurm && ./run_slurm.sh

## CSV file format

The results of each test will be logged to a corresponding CSV file with the 
following line format, depending on the type of test:

    run_number,current_samples,mh_time,mh_probability,gibbs_time,gibbs_probability

or

    run_number,current_samples,adapt_on_time,adapt_on_probability,adapt_off_time,adapt_off_probability

### Rules

- Each line ends with a line feed character (ASCII code 10).
- All running times are computed in milliseconds.

## Plot

The tools useful to plot the results are Python 3 and Matplotlib.

The plot script is in `./src/plot/plot_comparison.py`. This script reads
a CSV file formatted according to the CSV file format rules in this readme.
It then plots the average running times of multiple runs for each 
sample. The standard deviation of the running times for each sample is plotted 
as error bars. The same type of plot is done for the computed probabilities to 
determine the accuracy of the calculations.

## Notes on running the tests in parallel

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

The `plot_comparison.py` script sorts the data internally.

### An alternative to GNU Parallel

Use background processes.

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
