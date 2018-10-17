:- set_prolog_flag(verbose, silent).
:- initialization(main).
:- use_module(library(mcintyre)).

/* if min > max
 * or min == 0
 * or step <= 0
 * or min empty
 * or max empty
 * or step empty
 * or min not integer
 * or max not integer
 * or step not integer:
 *       fail
 */
main :-
    current_prolog_flag(argv, Argv),
    [Min_a|T] = Argv,
    [Max_a|U] = T,
    [Step_a|_] = U,
    atom_number(Min_a, Min),
    atom_number(Max_a, Max),
    atom_number(Step_a, Step),
    integer(Min),
    integer(Max),
    integer(Step),
    Min > 0,
    Step > 0,
    Min =< Max,
    format('Called with: Min=~q, Max=~q, Step=~q\n', [Min, Max, Step]),
    format('# samples\tmhs_time\tgbs_time\n'),
    loop(Min,Max,Step),
    halt.

main :-
    halt(1).

/* for i = $min, i < $max, i += step:
 *      samples = i
 *      time_mh = measure_mh(samples)
 *      time_gibbs = measure_gibbs(samples)
 *      print(samples, time_mh, time_gibbs)
 */
loop(Curr,Max,_):-
    Curr>Max,
    !.

loop(Curr, Max, Step):-
    Samples is Curr,
    measure_mh_arithm(Time_mh,Samples),
    measure_gibbs_arithm(Time_gibbs,Samples),
    format('~q\t~q\t~q\n', [Samples, Time_mh, Time_gibbs]),
    N is Curr+Step,
    loop(N,Max,Step).

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
