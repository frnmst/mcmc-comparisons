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
    /* Get and parse the CLI arguments. */
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
    format('performing arithm.pl on arithm_sample.csv\n'),
    [swish/examples/inference/arithm],
    open('arithm_sample.csv',write,Out_a),
    loop_arithm_sample(Min,Max,Step,Out_a),
    close(Out_a),
    format('performing arithm.pl on arithm_sample_arg.csv\n'),
    open('arithm_sample_arg.csv',write,Out_b),
    loop_arithm_sample_arg(Min,Max,Step,Out_b),
    close(Out_b),
    halt.

main :-
    halt(1).

/* for i = $min, i < $max, i += step:
 *      samples = i
 *      time_mh = measure_mh(samples)
 *      time_gibbs = measure_gibbs(samples)
 *      print(samples, time_mh, time_gibbs)
 */
loop_arithm_sample(Curr,Max,_,_):-
    Curr>Max,
    !.

/* format: samples\tmhs_time\tgbs_time\n' */
loop_arithm_sample(Curr, Max, Step, Out):-
    Samples is Curr,
    measure_arithm_mh_sample(Time_mh,Samples),
    measure_arithm_gibbs_sample(Time_gibbs,Samples),
    format('~q of ~q samples\n', [Samples, Max]),
    format(Out, '~q\t~q\t~q\n', [Samples, Time_mh, Time_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_arithm_sample(N,Max,Step,Out).

loop_arithm_sample_arg(Curr,Max,_,_):-
    Curr>Max,
    !.

loop_arithm_sample_arg(Curr, Max, Step, Out):-
    Samples is Curr,
    measure_arithm_mh_sample_arg(Time_mh,Samples),
    measure_arithm_gibbs_sample_arg(Time_gibbs,Samples),
    format('~q of ~q samples\n', [Samples, Max]),
    format(Out, '~q\t~q\t~q\n', [Samples, Time_mh, Time_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_arithm_sample_arg(N,Max,Step,Out).

measure_arithm_mh_sample(Time, Samples):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).

measure_arithm_gibbs_sample(Time, Samples):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(eval(2,4),eval(1,3),Samples,_,[mix(100),lag(3),successes(_),failures(_)]),
    statistics(walltime, [_|[Time]]).

measure_arithm_mh_sample_arg(Time, Samples):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample_arg(eval(2,_),(eval(0,2),eval(1,3)),Samples,_,_,[mix(100),lag(3)]),
    statistics(walltime, [_|[Time]]).

measure_arithm_gibbs_sample_arg(Time, Samples):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample_arg(eval(2,_),(eval(0,2),eval(1,3)),Samples,_,_,[mix(100),lag(3)]),
    statistics(walltime, [_|[Time]]).
