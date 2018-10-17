:- set_prolog_flag(verbose, silent).
:- initialization(main).
:- use_module(library(mcintyre)).

/* Ideas: 
 *
 * ./poc.pl $min $max $step
 *
 * for i = $min, i < $max, i += step:
 *       samples = i
 *       time_mh = measure_mh(samples)
 *       time_gibbs = measure_gibbs(samples)
 *       print(samples, time_mh, time_gibbs)
 */

main :-
    current_prolog_flag(argv, Argv),
    format('Called with ~q\n', [Argv]),
    format('\n'),
    append(_, [X], Argv),
    atom_number(X, Samples),
    measure_mh(Time_mh,Samples),
    measure_gibbs(Time_gibbs,Samples),
    format('# samples\tmhs_time\tgbs_time\n'),
    format('~q\t~q\t~q\n', [Samples, Time_mh, Time_gibbs]),
    halt.

main :-
    halt(1).

measure_mh(Time, Samples):-
    [swish/examples/inference/arithm],
    statistics(walltime, [_|[_]]),
    mc_mh_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).

measure_gibbs(Time, Samples):-
    [swish/examples/inference/arithm],
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).
