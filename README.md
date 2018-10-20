# mcmc-comparisons

comparision of various [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) 
algorithms in SWI Prolog

## Algorithms

- [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm)
- [Gibbs sampling](https://en.wikipedia.org/wiki/Gibbs_sampling)

## Instructions

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

- Clone the repository with the swish git submodule:

      $ git clone --recurse-submodules https://github.com/frnmst/mcmc-comparisons.git

- Execute the `run.sh` script.

      help: ./run.sh min max samples

## CSV file format

The results of each test will be logged to a corresponding CSV file with the 
following line format:

    run_number,current_samples,mh_time,gibbs_time

Each line ends with a line feed character (ASCII code 10).

## License

See the `LICENSE` file.
