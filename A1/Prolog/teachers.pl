subject(algebra,            math).
subject(calculus,           math).
subject(dynamics,           physics).
subject(electromagnetism,   physics).
subject(nuclear,            physics).
subject(organic,            chemistry).
subject(inorganic,          chemistry).

degree(bill,    phd,    chemistry).
degree(john,    bs,     math).
degree(chuck,   ms,     physics).
degree(susan,   phd,    math).

retired(bill).

% X can teach class Y only if they have a PhD in the subject matter
canTeach(X,Y) :-
    degree(X, phd, Z),
    subject(Y, Z).

% X can teach class Y only if they have a PhD or MS in the subject matter
canTeach2(X,Y) :-
    (degree(X, phd, Z); degree(X, ms, Z)),
    subject(Y, Z).
    
% X can teach class Y only if they have a PhD or MS in the subject matter and are not retired
canTeach3(X,Y) :-
    (degree(X, phd, Z); degree(X, ms, Z)),
    subject(Y, Z),
    \+ retired(X).