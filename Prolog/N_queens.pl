% N-queens problem

:- use_module(library(clpfd)).

n_queens(N, Qs) :-
    length(Qs, N),        % N variables (one per row)
    Qs ins 1..N,          % domain: columns 1..N
    all_distinct(Qs),     % no two queens in same column
    diagonal_constraints(Qs),
    labeling([ff], Qs).   % search strategy (first-fail)

diagonal_constraints([]).
diagonal_constraints([Q|Qs]) :-
    safe_from(Q, Qs, 1),
    diagonal_constraints(Qs).

safe_from(_, [], _).
safe_from(Q, [Q2|Qs], D) :-
    abs(Q - Q2) #\= D,    % not on same diagonal
    D1 #= D + 1,
    safe_from(Q, Qs, D1).