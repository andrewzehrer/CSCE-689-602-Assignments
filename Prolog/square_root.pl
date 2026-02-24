sqrt(0, 0).

sqrt(X, Y) :-
    X > 0,
    InitialGuess is X / 2,
    Tolerance is 0.0000000001,
    newton_iter(X, InitialGuess, Tolerance, Y).

newton_iter(X, Guess, Tolerance, Result) :-
    Next is 0.5 * (Guess + X / Guess),
    Diff is abs(Next - Guess),
    (Diff < Tolerance ->  Result = Next; newton_iter(X, Next, Tolerance, Result)).