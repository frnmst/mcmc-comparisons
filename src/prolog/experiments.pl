/* expriments.pl
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
    parse_cli_args(Argv,Experiment_name,Output_file,Min,Max,Step,Runs,Parallel),
    format('Called with: Experiment_name=~q, Output_file=~q, Min=~q, Max=~q, Step=~q, Runs=~q, Parallel=~q\n', [Experiment_name, Output_file, Min, Max, Step, Runs, Parallel]),
    select_experiment(Experiment_name,Output_file,Min,Max,Step,Runs,Parallel),
    halt.

main :-
    halt(1).

/* Select experiment and if it is sequential or parallel (single).
 * See http://cs.union.edu/~striegnk/learn-prolog-now/html/node89.html
 * for the if-then-else clauses.
 */
select_experiment(Experiment_name,Output_file,Min,Max,Step,Runs,Parallel):-
    Parallel == 1,
    !,
    atom_string("arithm_sample",A),
    atom_string("arithm_sample_three",B),
    atom_string("arithm_rejection_sample",C),
    atom_string("test33_sample",D),
    atom_string("test66_sample",E),
    atom_string("hmm_sample_three",F),
    ( A = Experiment_name
      -> experiments_single_arithm_sample(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( B = Experiment_name
      -> experiments_single_arithm_sample_three(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( C = Experiment_name
      -> experiments_single_arithm_rejection_sample(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( D = Experiment_name
      -> experiments_single_test33(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( E = Experiment_name
      -> experiments_single_test66(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( F = Experiment_name
      -> experiments_single_hmm_sample_three(Output_file,Min,Max,Step,Runs)
    ).

select_experiment(Experiment_name,Output_file,Min,Max,Step,Runs,_):-
    atom_string("arithm_sample",A),
    atom_string("arithm_rejection_sample",B),
    atom_string("test33_sample",C),
    atom_string("test66_sample",D),
    atom_string("arithm_sample_three",E),
    atom_string("hmm_sample_three",F),
    ( A = Experiment_name
      -> experiments_sequential_arithm(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( B = Experiment_name
      -> experiments_sequential_arithm_rejection_sample(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( C = Experiment_name
      -> experiments_sequential_test33(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( D = Experiment_name
      -> experiments_sequential_test66(Output_file,Min,Max,Step,Runs)
      ; 1 = 1
    ),
    ( E = Experiment_name
      -> writeln('not implemented')
      ; 1 = 1
    ),
    ( F = Experiment_name
      -> writeln('not implemented')
    ).

/* Check that all the Argv values are integers with some conditions. */
is_parallel(Parallel):-
    Parallel == 1.

is_parallel(Parallel):-
    Parallel == 0.

parse_cli_args(Argv,Experiment_name,Output_file,Min,Max,Step,Runs,Parallel):-
    [Experiment_name_a|S] = Argv,
    [Output_file_a|T] = S,
    [Min_a|U] = T,
    [Max_a|V] = U,
    [Step_a|W] = V,
    [Runs_a|X] = W,
    [Parallel_a|_] = X,

    atom_string(Experiment_name_a, Experiment_name),
    atom_string(Output_file_a, Output_file),
    atom_number(Min_a, Min),
    atom_number(Max_a, Max),
    atom_number(Step_a, Step),
    atom_number(Runs_a, Runs),
    atom_number(Parallel_a, Parallel),

    string(Experiment_name),
    string(Output_file),
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

/* arithm sample */

experiments_single_arithm_sample(Output_file,Min,Max,Step,Run_label):-
    format('performing arithm.pl on ~q\n', Output_file),
    ['../prolog/swish/examples/inference/arithm'],
    open(Output_file,append,Out_a),
    loop_arithm_sample(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

experiments_sequential_arithm_sample(_,_,_,_,Runs):-
    Runs=<0,
    !.

experiments_sequential_arithm_sample(Output_file,Min,Max,Step,Runs):-
    experiments_single_arithm_sample(Output_file,Min,Max,Step,Runs),
    N is Runs-1,
    experiments_sequential_arithm_sample(Output_file,Min,Max,Step,N).

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

measure_arithm_mh_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(eval(2,4),eval(1,3),Samples,Prob,[mix(100),lag(3)]),
    statistics(walltime, [_|[Time]]).

measure_arithm_gibbs_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(eval(2,4),eval(1,3),Samples,Prob,[mix(100)]),
    statistics(walltime, [_|[Time]]).

/* arithm rejection sample */

experiments_single_arithm_rejection_sample(Output_file,Min,Max,Step,Run_label):-
    format('performing arithm.pl on ~q\n', Output_file),
    ['../prolog/swish/examples/inference/arithm'],
    open(Output_file,append,Out_a),
    loop_arithm_rejection_sample(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

experiments_sequential_arithm_rejection_sample(_,_,_,_,Runs):-
    Runs=<0,
    !.

experiments_sequential_arithm_rejection_sample(Min,Max,Step,Runs):-
    experiments_single_arithm_rejection_sample(Min,Max,Step,Runs),
    N is Runs-1,
    experiments_sequential_arithm_rejection_sample(Min,Max,Step,N).

loop_arithm_rejection_sample(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_arithm_rejection_sample(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_arithm_rejection_sample(Time_mh,Samples,P_mh),
    measure_arithm_gibbs_sample(Time_gibbs,Samples,P_gibbs),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh, P_mh, Time_gibbs, P_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_arithm_rejection_sample(N,Max,Step,Runs,Out).

measure_arithm_rejection_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_rejection_sample(eval(2,4),eval(1,3),Samples,Prob,[mix(100)]),
    statistics(walltime, [_|[Time]]).

/* test33 */

experiments_single_test33(Output_file,Min,Max,Step,Run_label):-
    format('performing test33.pl on ~q\n', Output_file),
    ['../prolog/amcmc/swi/test33'],
    open(Output_file,append,Out_a),
    loop_test33_sample(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

experiments_sequential_test33(_,_,_,Runs):-
    Runs=<0,
    !.

experiments_sequential_test33(Min,Max,Step,Runs):-
    experiments_single_test33(Min,Max,Step,Runs),
    N is Runs-1,
    experiments_sequential_test33(Min,Max,Step,N).

loop_test33_sample(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_test33_sample(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_test33_mh_sample(Time_mh,Samples,P_mh),
    measure_test33_gibbs_sample(Time_gibbs,Samples,P_gibbs),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh, P_mh, Time_gibbs, P_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_test33_sample(N,Max,Step,Runs,Out).

measure_test33_mh_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(t(query),t(evidence),Samples,Prob,[]),
    statistics(walltime, [_|[Time]]).

measure_test33_gibbs_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(t(query),t(evidence),Samples,Prob,[]),
    statistics(walltime, [_|[Time]]).

/* test66 */

experiments_single_test66(Output_file,Min,Max,Step,Run_label):-
    format('performing test66.pl on ~q\n', Output_file),
    ['../prolog/amcmc/swi/test66'],
    open(Output_file,append,Out_a),
    loop_test66_sample(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

experiments_sequential_test66(_,_,_,Runs):-
    Runs=<0,
    !.

experiments_sequential_test66(Min,Max,Step,Runs):-
    experiments_single_test66(Min,Max,Step,Runs),
    N is Runs-1,
    experiments_sequential_test66(Min,Max,Step,N).

loop_test66_sample(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_test66_sample(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_test66_mh_sample(Time_mh,Samples,P_mh),
    measure_test66_gibbs_sample(Time_gibbs,Samples,P_gibbs),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh, P_mh, Time_gibbs, P_gibbs]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_test66_sample(N,Max,Step,Runs,Out).

measure_test66_mh_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(t(query),t(evidence),Samples,Prob,[]),
    format('here\n'),
    statistics(walltime, [_|[Time]]).

measure_test66_gibbs_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(t(query),t(evidence),Samples,Prob,[]),
    statistics(walltime, [_|[Time]]).


/*************************
 * Three way comparisons *
 *************************/

/* arithm_sample */

experiments_single_arithm_sample_three(Output_file,Min,Max,Step,Run_label):-
    format('performing arithm_sample_three.pl on ~q\n', Output_file),
    ['../prolog/swish/examples/inference/arithm.pl'],
    open(Output_file,append,Out_a),
    loop_arithm_sample_three(Min,Max,Step,Run_label,Out_a),
    close(Out_a).

loop_arithm_sample_three(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_arithm_sample_three(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_arithm_mh_sample(Time_mh_sample,Samples,P_mh_sample),
    measure_arithm_gibbs_sample(Time_gibbs_sample,Samples,P_gibbs_sample),
    measure_arithm_rejection_sample(Time_rejection_sample,Samples,P_rejection_sample),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh_sample, P_mh_sample, Time_gibbs_sample, P_gibbs_sample, Time_rejection_sample, P_rejection_sample]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_arithm_sample_three(N,Max,Step,Runs,Out).

/* hmm */

experiments_single_hmm_sample_three(Output_file,Min,Max,Step,Run_label):-
    format('performing hmm_sample_three.pl on ~q\n', Output_file),
    ['../prolog/swish/examples/inference/hmm.pl'],
    open(Output_file,append,Out_a),
    loop_hmm_sample_three(Min,Max,Step,Run_label,Out_a),
    close(Out_a).


loop_hmm_sample_three(Curr,Max,_,_,_):-
    Curr>Max,
    !.

loop_hmm_sample_three(Curr, Max, Step, Runs, Out):-
    Samples is Curr,
    measure_hmm_mh_sample(Time_mh,Samples,P_mh),
    measure_hmm_gibbs_sample(Time_gibbs,Samples,P_gibbs),
    measure_hmm_rejection_sample(Time_rejection,Samples,P_rejection),
    format('run ~q, sample ~q of ~q\n', [Runs, Samples, Max]),
    format(Out, '~q,~q,~q,~q,~q,~q,~q,~q\n', [Runs, Samples, Time_mh, P_mh, Time_gibbs, P_gibbs, Time_rejection, P_rejection]),
    flush_output(Out),
    flush_output,
    N is Curr+Step,
    loop_hmm_sample_three(N,Max,Step,Runs,Out).

measure_hmm_mh_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_mh_sample(hmm([a,c]),letter(q1,a,1),Samples,Prob,[mix(100)]),
    statistics(walltime, [_|[Time]]).

measure_hmm_gibbs_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_gibbs_sample(hmm([a,c]),letter(q1,a,1),Samples,Prob,[mix(100)]),
    statistics(walltime, [_|[Time]]).

measure_hmm_rejection_sample(Time, Samples, Prob):-
    statistics(walltime, [_|[_]]),
    mc_rejection_sample(hmm([a,c]),letter(q1,a,1),Samples,Prob,[mix(100)]),
    statistics(walltime, [_|[Time]]).
