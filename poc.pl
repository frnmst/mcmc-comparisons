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
    format('# samples\tmhs_time\tgbs_time\n'),
    format('\n'),
    append(_, [X], Argv),
    atom_number(X, Min),
    append(_, [Y], Argv),
    atom_number(Y, Step),
    loop(Min,Step),
    halt.

main :-
    halt(1).

/* loop(max,_) */
loop(N,_):-
    N>=26,
    !.

loop(N, Step):-
    Samples is N,
    measure_mh_arithm(Time_mh,Samples),
    measure_gibbs_arithm(Time_gibbs,Samples),
    format('~q\t~q\t~q\n', [Samples, Time_mh, Time_gibbs]),
    N1 is N+Step,
    loop(N1,Step).

measure_mh_arithm(Time, Samples):-
    [swish/examples/inference/arithm],
    statistics(walltime, [_|[_]]),
    mc_mh_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).

measure_gibbs_arithm(Time, Samples):-
    [swish/examples/inference/arithm],
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).
