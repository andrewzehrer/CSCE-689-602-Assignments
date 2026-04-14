%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Board Representation  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% empty board
initial_board([e,e,e,e,e,e,e,e,e]).

% switch player
other_player(x, o).
other_player(o, x).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%     Win Conditions     %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

win(Board, P) :-
    winning_line(A,B,C),
    nth1(A, Board, P),
    nth1(B, Board, P),
    nth1(C, Board, P),
    P \= e.

winning_line(1,2,3).
winning_line(4,5,6).
winning_line(7,8,9).
winning_line(1,4,7).
winning_line(2,5,8).
winning_line(3,6,9).
winning_line(1,5,9).
winning_line(3,5,7).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%       Terminal         %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

full(Board) :-
    \+ member(e, Board).

terminal(Board, x,  1) :- 
    win(Board, x).

terminal(Board, o, -1) :- 
    win(Board, o).

terminal(Board, _,  0) :- 
    full(Board),
    \+ win(Board, x),
    \+ win(Board, o).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%       Legal Moves      %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

legal_move(Board, Index) :-
    nth1(Index, Board, e).

make_move(Board, Index, Player, NewBoard) :-
    legal_move(Board, Index),
    replace(Board, Index, Player, NewBoard).

replace([_|T], 1, X, [X|T]).
replace([H|T], I, X, [H|R]) :-
    I > 1,
    I1 is I - 1,
    replace(T, I1, X, R).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%        Minimax         %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

minimax(Board, Player, BestMove) :-
    findall(M, legal_move(Board, M), Moves),
    choose_best(Moves, Board, Player, BestMove, _).

choose_best([Move], Board, Player, Move, Score) :-
    make_move(Board, Move, Player, NewBoard),
    minimax_value(NewBoard, Player, Score), !.

choose_best([Move|Moves], Board, Player, BestMove, BestScore) :-
    make_move(Board, Move, Player, NewBoard),
    minimax_value(NewBoard, Player, Score),
    choose_best(Moves, Board, Player, TempMove, TempScore),
    better(Player, Move, Score, TempMove, TempScore,
           BestMove, BestScore).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%     Minimax Value      %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Terminal positions
minimax_value(Board, _, 1) :-
    win(Board, x), !.

minimax_value(Board, _, -1) :-
    win(Board, o), !.

minimax_value(Board, _, 0) :-
    full(Board), !.

% Recursive case
minimax_value(Board, Player, Score) :-
    other_player(Player, Opponent),
    findall(M, legal_move(Board, M), Moves),
    evaluate_moves(Moves, Board, Opponent, Scores),
    best_score(Opponent, Scores, Score).

evaluate_moves([], _, _, []).
evaluate_moves([Move|Moves], Board, Player, [Score|Scores]) :-
    make_move(Board, Move, Player, NewBoard),
    minimax_value(NewBoard, Player, Score),
    evaluate_moves(Moves, Board, Player, Scores).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%    Score Selection     %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% If it's X's turn, X wants max
best_score(x, Scores, Score) :-
    max_list(Scores, Score).

% If it's O's turn, O wants min
best_score(o, Scores, Score) :-
    min_list(Scores, Score).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%    Move Comparison     %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

better(x, Move, Score, _, TempScore, Move, Score) :-
    Score > TempScore, !.

better(o, Move, Score, _, TempScore, Move, Score) :-
    Score < TempScore, !.

better(_, _, _, TempMove, TempScore, TempMove, TempScore).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%        Play Loop       %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

play(Board, Player) :-
    print_board(Board),
    ( 
        win(Board, x) -> writeln('You (X) win! 🎉');
        win(Board, o) -> writeln('Computer (O) wins!'); 
        full(Board) -> writeln('It''s a draw.');
        ( 
            Player = x -> human_move(Board, Move);
            minimax(Board, o, Move), format('Computer plays at position ~w~n', [Move])
        ),
        make_move(Board, Move, Player, NewBoard),
        other_player(Player, Next),
        play(NewBoard, Next)
    ).

human_move(Board, Move) :-
    write('Enter your move (1-9): '),
    read(Move),
    ( 
        integer(Move),
        between(1,9,Move),
        legal_move(Board, Move) -> true;
        writeln('Invalid move. Try again.'),
        human_move(Board, Move)
    ).


print_board([A,B,C,D,E,F,G,H,I]) :-
    display_cell(A), write(' | '),
    display_cell(B), write(' | '),
    display_cell(C), nl,
    write('---+---+---'), nl,
    display_cell(D), write(' | '),
    display_cell(E), write(' | '),
    display_cell(F), nl,
    write('---+---+---'), nl,
    display_cell(G), write(' | '),
    display_cell(H), write(' | '),
    display_cell(I), nl, nl.

display_cell(e) :- write(' ').
display_cell(X) :- write(X).