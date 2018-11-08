/* tests.pl
 *
 * BSD 2-Clause License
 *
 * Copyright (c) 2018, Franco Masotti
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *  * Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

:- set_prolog_flag(verbose, silent).
:- initialization(main).
:- use_module(library(mcintyre)).

main :-
    current_prolog_flag(argv, Argv),
    parse_cli_args(Argv,Min,Max,Step,Runs,Parallel),
    format('Called with: Min=~q, Max=~q, Step=~q, Runs=~q, Parallel=~q\n', [Min, Max, Step, Runs, Parallel]),
    sequential_or_parallel_tests(Min,Max,Step,Runs,Parallel),
    halt.

main :-
    halt(1).

/* Select sequential or parallel (single) test runs. */
sequential_or_parallel_tests(Min,Max,Step,Runs,Parallel):-
    Parallel == 1,
    !,
    tests_single(Min,Max,Step,Runs).

sequential_or_parallel_tests(Min,Max,Step,Runs,_):-
    tests_sequential(Min,Max,Step,Runs).

/* Check that all the Argv values are integers with some conditions. */
is_parallel(Parallel):-
    Parallel == 1.

is_parallel(Parallel):-
    Parallel == 0.

parse_cli_args(Argv,Min,Max,Step,Runs,Parallel):-
    [Min_a|T] = Argv,
    [Max_a|U] = T,
    [Step_a|V] = U,
    [Runs_a|W] = V,
    [Parallel_a|_] = W,
    atom_number(Min_a, Min),
    atom_number(Max_a, Max),
    atom_number(Step_a, Step),
    atom_number(Runs_a, Runs),
    atom_number(Parallel_a, Parallel),
    integer(Min),
    integer(Max),
    integer(Step),
    integer(Runs),
    integer(Parallel),
    Min > 0,
    Step > 0,
    Runs > 0,
    is_parallel(Parallel),
    Min =< Max.

/* for j = 0, j < $runs, j++:
 *      for i = $min, i < $max, i += $step:
 *          samples = i
 *          time_mh = measure_mh(samples)
 *          time_gibbs = measure_gibbs(samples)
 *          print(samples, time_mh, time_gibbs)
 */
tests_single(Min,Max,Step,Run_label):-
    format('performing arithm.pl on arithm_sample.csv\n'),
    [swish/examples/inference/arithm],
    open('arithm_sample.csv',append,Out_a),
    loop_arithm_sample(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

tests_sequential(_,_,_,Runs):-
    Runs=<0,
    !.

tests_sequential(Min,Max,Step,Runs):-
    tests_single(Min,Max,Step,Runs),
    N is Runs-1,
    tests_sequential(Min,Max,Step,N).

loop_arithm_sample(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_arithm_sample(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_arithm_mh_sample(Time_mh,Samples,P_mh),
    measure_arithm_gibbs_sample(Time_gibbs,Samples,P_gibbs),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh, P_mh, Time_gibbs, P_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_arithm_sample(N,Max,Step,Runs,Out).

loop_arithm_sample_arg(Curr,Max,_,_):-
    Curr>Max,
    !.

measure_arithm_mh_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(eval(2,4),eval(1,3),Samples,Prob,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).

measure_arithm_gibbs_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(eval(2,4),eval(1,3),Samples,Prob,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).
