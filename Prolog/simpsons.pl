parent(bart,homer).
parent(bart,marge).
parent(lisa,homer).
parent(lisa,marge).
parent(maggie,homer).
parent(maggie,marge).
parent(homer,abraham).
parent(herb,abraham).
parent(tod,ned).
parent(rod,ned).
parent(marge,jackie).
parent(patty,jackie).
parent(selma,jackie).

female(maggie).
female(lisa).
female(marge).
female(patty).
female(selma).
female(jackie).

male(bart).
male(homer).
male(herb).
male(burns).
male(smithers).
male(tod).
male(rod).
male(ned).
male(abraham).



% Y is a male parent of X
father(X,Y) :-
    male(Y),
    parent(X,Y).

% Y is a female parent of X
mother(X,Y) :-
    female(Y),
    parent(X,Y).

% Y is a child of X
child(X,Y) :-
    parent(Y,X).

% Y is a male child of X
son(X,Y) :-
    male(Y),
    child(X,Y).

% Y is a female child of X
daughter(X,Y) :-
    female(Y),
    child(X,Y).

% X and Y share at least one parent and are not the same person
sibling(X,Y) :-
    parent(X,Z),
    parent(Y,Z),
    X \== Y.

% Y is a male sibling of X
brother(X,Y) :-
    male(Y),
    sibling(X,Y).

% Y is a female sibling of X
sister(X,Y) :-
    female(Y),
    sibling(X,Y).

% Y is a male child of X's sibling
nephew(X,Y) :-
    male(Y),
    parent(Y,Z),
    sibling(Z,X).

% Y is a female child of X's sibling
niece(X,Y) :-
    female(Y),
    parent(Y,Z),
    sibling(Z,X).

% Y is a brother of X's parent
uncle(X,Y) :-
    parent(X,Z),
    brother(Z,Y).

% Y is a sister of X's parent
aunt(X,Y) :-
    parent(X,Z),
    sister(Z,Y).

% Y is a parent of X's parent
grandparent(X,Y) :-
    parent(X,Z),
    parent(Z,Y).

% Y is a male grandparent of X
grandfather(X,Y) :-
    male(Y),
    grandparent(X,Y).

% Y is a female grandparent of X
grandmother(X,Y) :-
    female(Y),
    grandparent(X,Y).

% Y is a child of X's child
grandchild(X,Y) :-
    child(X,Z),
    child(Z,Y).

% Y is a male grandchild of X
grandson(X,Y) :-
    male(Y),
    grandchild(X,Y).

% Y is a female grandchild of X
granddaughter(X,Y) :-
    female(Y),
    grandchild(X,Y).

% Y is a parent or grandparent of X
ancestor(X,Y) :-
    parent(X,Y);
    grandparent(X,Y).

% Y is a child or grandchild of X
descendant(X,Y) :-
    child(X,Y);
    grandchild(X,Y).

% Y is X, or is a parent, child, sibling, grandparent, grandchild, aunt, uncle, niece, or nephew of X
related(X,Y) :-
    X == Y;
    parent(X,Y);
    child(X,Y);
    sibling(X,Y);
    grandparent(X,Y);
    grandchild(X,Y);
    aunt(X,Y);
    uncle(X,Y);
    niece(X,Y);
    nephew(X,Y).

% Y is not related to X
unrelated(X,Y) :-
    \+ related(X,Y).
