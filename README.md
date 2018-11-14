# mcmc-comparisons

comparision of various [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) 
algorithms in SWI Prolog

## Table of contents

[](TOC)

- [mcmc-comparisons](#mcmc-comparisons)
    - [Table of contents](#table-of-contents)
    - [Installation](#installation)
    - [Running](#running)
        - [Run locally](#run-locally)
            - [Sequential version](#sequential-version)
            - [Parallel version](#parallel-version)
        - [Run on a SLURM queue](#run-on-a-slurm-queue)
    - [CSV file format](#csv-file-format)
    - [Plot](#plot)
    - [Notes on running the tests is parallel](#notes-on-running-the-tests-is-parallel)
        - [Output files](#output-files)
        - [An alternative to GNU Parallel](#an-alternative-to-gnu-parallel)
    - [References](#references)
        - [SLURM](#slurm)
    - [License](#license)

[](TOC)

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

- Install [Python 3](http://www.python.org/), 
  [Matplotlib](https://matplotlib.org/) and
  [NumPy](http://www.numpy.org/).

- Install [GNU Parallel](http://www.gnu.org/software/parallel/)

- Clone the repository with the swish git submodule:

      $ git clone --recurse-submodules https://github.com/frnmst/mcmc-comparisons.git

## Running

### Run locally

- Go to the local directory

      $ cd src/local

- Execute the `run.sh` script, for example like this:

      $ ./run.sh -p 1 10001 1000 4

#### Sequential version

    $ ./run.sh min max samples runs

#### Parallel version

    $ ./run.sh -p min max samples threads

where `threads` corresponds to the number of concurrent `runs`. This will speed 
up multiple runs but it will use more memory.

### Run on a SLURM queue

The purpose of using SLURM is to run the tests in parallel.

- Go to the slurm directory and run the shell file

      $ cd src/slurm && sbatch run_slurm.sh

- You may also run the test interactively

      $  cd src/slurm && ./run_slurm.sh

## CSV file format

The results of each test will be logged to a corresponding CSV file with the 
following line format:

    run_number,current_samples,mh_time,mh_probability,gibbs_time,gibbs_probability

Each line ends with a line feed character (ASCII code 10).

Running times are computed in milliseconds.

## Plot

The tools useful to plot the results are Python 3 and Matplotlib.

The plot script is in `./src/plot/plot_comparison.py`. This script reads
a CSV file and plots the average running times of multiple runs for each 
sample. The standard deviation of the running times for each sample is plotted 
as error bars.

## Notes on running the tests is parallel

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

- [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm)
- [Gibbs sampling](https://en.wikipedia.org/wiki/Gibbs_sampling)

### SLURM

- [SLURM](https://slurm.schedmd.com/)
- [SLURM serial jobs](https://www.chpc.utah.edu/documentation/software/serial-jobs.php)
- [SLURM Multi Program Usage](https://www.tchpc.tcd.ie/node/167)
- [SLURM configurator tool](https://slurm.schedmd.com/configurator.html)
- [The Slurm job scheduler](http://www.arc.ox.ac.uk/content/slurm-job-scheduler)
- [Slurm - Arch Wiki](https://wiki.archlinux.org/index.php/Slurm)

## License

See the `LICENSE` file.
