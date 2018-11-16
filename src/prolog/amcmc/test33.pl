:- use_module(library(mcintyre)).
:- mc.
:- begin_lpad.
% dim(3,3)
% query([(2  ','  2)],[t])
% evidence([(1  ','  2),(2  ','  3)],[t,t])
% file(test33.psm)
world(A,B,C,D,E,F,G,H,I) :-
    f(1,1,0,0,A),          
    f(1,2,0,A,B),
    f(1,3,0,B,C),
    f(2,1,A,0,D),
    f(2,2,B,D,E),
    f(2,3,C,E,F),
    f(3,1,D,0,G),
    f(3,2,E,G,H),
    f(3,3,F,H,I).

query(A) :-
    world(B,C,D,E,A,F,G,H,I).

evidence(A,B) :-
    world(C,A,D,E,F,B,G,H,I).

t(query) :-
    query(t).
t(evidence) :-
    evidence(t,t).

q(A) :-
    world(C,t,D,E,A,t,G,H,I).

f(1,1,0,0,A):discrete(A,[t:0.0100,f:0.9900]).
f(1,2,0,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(1,2,0,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(1,3,0,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(1,3,0,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,1,t,0,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,1,f,0,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,2,t,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,2,t,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,2,f,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,2,f,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,3,t,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,3,t,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,3,f,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(2,3,f,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,1,t,0,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,1,f,0,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,2,t,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,2,t,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,2,f,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,2,f,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,3,t,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,3,t,f,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,3,f,t,A):discrete(A,[t:0.0100,f:0.9900]).
f(3,3,f,f,A):discrete(A,[t:0.0100,f:0.9900]).

:-end_lpad.

