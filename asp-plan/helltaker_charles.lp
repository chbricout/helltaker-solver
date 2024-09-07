%% constantes 
action(
    move;
    movePique;
    movePiege; 
    pushBlocCase; 
    pushBlocMur; 
    pushBlocImmo; 
    pushMobCase; 
    pushMobMur; 
    pushMobKill; 
    moveKey; 
    openDoor).

%directions
direction(
    up;
    down;
    left; 
    right).

step(0..n).


%prédicats successeurs
succ(up,pos(X,Y), pos(X,Y2)):-
    case(pos(X,Y)),
    case(pos(X,Y-1)),
    Y2=Y-1.

succ(down,pos(X,Y), pos(X,Y2)):-
    case(pos(X,Y)),
    case(pos(X,Y2)),
    Y2=Y+1.

succ(right,pos(X,Y), pos(X2,Y)):-
    case(pos(X,Y)),
    case(pos(X2,Y)),
    X2=X+1.

succ(left,pos(X,Y), pos(X2,Y)):-
    case(pos(X,Y)),
    case(pos(X2,Y)),
    X2=X-1.

%% On genere un seul but 
{goal(me(P)):
    demone(P2),
    succ(_, P,P2)}=1.

fluent(actionRestante(n), 0).


:- goal(me(P)), not fluent(me(P), _).
:- goal(me(P)), fluent(me(P), T), do(_, T+1).

% obligation d'avoir une position
:-  do(action(_,_),T), 
    not fluent(me(_),T+1).

:-  do(action(_,_),T), 
    fluent(actionRestante(X),T), 
    not X>0.


%switch des traps
fluent(piege(P, true), T+1):-
    fluent(piege(P, false), T),
    step(T).

fluent(piege(P, false), T+1):-
    fluent(piege(P, true), T),
    step(T).


{do(action(M,D), T): 
action(M),
direction(D)}1 :- step(T).

%% action move
% preconditions
:-  do(action(move, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(move, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2),
    not fluent(me(P2),T+1).

:-  do(action(move, D),T), 
    fluent(me(P), T+1), 
    pique(P).

:-  do(action(move, D),T), 
    fluent(me(P), T+1), 
    fluent(porte(P, true), T).

:-  do(action(move, D),T), 
    fluent(me(P), T+1), 
    fluent(mob(P),T).

:-  do(action(move, D),T), 
    fluent(me(P), T+1), 
    fluent(bloc(P),T).

:-  do(action(move, D),T),
    fluent(me(P), T+1),
    fluent(piege(P,true),T+1).

:-  do(action(move, D),T), 
    fluent(me(P), T+1), 
    fluent(cle(P, true),T).



% effets
fluent(me(P2), T):-
    do(action(move, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2).

removed(me(P),T):-
    do(action(move, D), T),
    fluent(me(P), T).

%% action movePique
% preconditions
:-  do(action(movePique, D),T),
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(movePique, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2), 
    not fluent(me(P2),T+1).

:-  do(action(movePique, D),T), 
    fluent(me(P), T+1), 
    not pique(P).

:-  do(action(movePique, D),T), 
    fluent(me(P), T+1),
    fluent(bloc(P),T+1).


% effets
fluent(me(P2), T):-
    do(action(movePique, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2).


removed(me(P),T):-
    do(action(movePique, D), T),
    fluent(me(P), T).

%% action movePiege
% preconditions
:-  do(action(movePiege, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(movePiege, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2), 
    not fluent(me(P2),T+1).


:-  do(action(movePiege, D),T), 
    fluent(me(P), T+1), 
    fluent(bloc(P),T).

:-  do(action(movePiege, D),T), 
    fluent(me(P), T+1), 
    not fluent(piege(P,true),T+1).

% effets
fluent(me(P2), T):-
    do(action(movePiege, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2).


removed(me(P),T):-
    do(action(movePiege, D), T),
    fluent(me(P), T).

%% action pushBlocCase
% preconditions
:-  do(action(pushBlocCase, D),T), 
    fluent(me(P), T),
     not succ(D, P, _).

:-  do(action(pushBlocCase, D),T),
    fluent(me(P), T),
    succ(D, P, P2), 
    not fluent(bloc(P2),T).


:-  do(action(pushBlocCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    not succ(D,P2,_).

:-  do(action(pushBlocCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(bloc(P3),T).

:-  do(action(pushBlocCase, D),T),
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(porte(P3, true),T).

:-  do(action(pushBlocCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(mob(P3),T).

:- do(action(pushBlocCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    demone(P3).



% effets
fluent(me(P), T):-
    do(action(pushBlocCase, D), T-1),
    fluent(me(P), T-1).

fluent(bloc(P3), T):-
    do(action(pushBlocCase, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2),
    succ(D,P2,P3).


removed(bloc(P2),T):-
    do(action(pushBlocCase, D), T),
    fluent(me(P), T),
    succ(D, P, P2),
    fluent(bloc(P2), T).

%% action pushBlocMur
% preconditions
:-  do(action(pushBlocMur, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(pushBlocMur, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2), 
    not fluent(bloc(P2),T).

:-  do(action(pushBlocMur, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    succ(D,P2,_).



% effets
fluent(me(P), T):-
    do(action(pushBlocMur, D), T-1),
    fluent(me(P), T-1).

fluent(bloc(P2), T):-
    do(action(pushBlocMur, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2).


removed(bloc(P2),T):-
    do(action(pushBlocMur, D), T),
    fluent(me(P), T),
    succ(D, P, P2).


%% action pushBlocImmo
% preconditions
:-  do(action(pushBlocImmo, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(pushBlocImmo, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2), 
    not fluent(bloc(P2),T).

:-  do(action(pushBlocImmo, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not succ(D,P2,_).

:-  do(action(pushBlocImmo, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    not fluent(porte(P3, true), T), 
    not fluent(mob(P3),T), 
    not fluent(bloc(P3),T),
    not demone(P3).


% effets
fluent(me(P), T):-
    do(action(pushBlocImmo, D), T-1),
    fluent(me(P), T-1).

fluent(bloc(P2), T):-
    do(action(pushBlocImmo, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2).


removed(bloc(P2),T):-
    do(action(pushBlocImmo, D), T),
    fluent(me(P), T),
    succ(D, P, P2).


%% action pushMobCase
% preconditions
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not fluent(mob(P2),T).

:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    not succ(D,P2,_).

:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),   
    succ(D,P2,P3), 
    fluent(bloc(P3),T).
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(porte(P3, true),T).
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(mob(P3),T).
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    fluent(piege(P3,true),T+1).
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    pique(P3).
:-  do(action(pushMobCase, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3), 
    demone(P3).



% effets
fluent(me(P), T):-
    do(action(pushMobCase, D), T-1),
    fluent(me(P), T-1).

fluent(mob(P3), T):-
    do(action(pushMobCase, D), T-1),
    fluent(me(P), T-1),
    succ(D, P, P2),
    succ(D,P2,P3).


removed(mob(P2),T):-
    do(action(pushMobCase, D), T),
    fluent(me(P), T),
    succ(D, P, P2),
    fluent(mob(P2), T).

%% action pushMobMur
% preconditions
:-  do(action(pushMobMur, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(pushMobMur, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not fluent(mob(P2),T).

:-  do(action(pushMobMur, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    succ(D,P2,_).



% effets
fluent(me(P), T):-
    do(action(pushMobMur, D), T-1),
    fluent(me(P), T-1).



removed(mob(P2),T):-
    do(action(pushMobMur, D), T),
    fluent(me(P), T),
    succ(D, P, P2).

%% action pushMobKill
% preconditions
:-  do(action(pushMobKill, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(pushMobKill, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not fluent(mob(P2),T).

:-  do(action(pushMobKill, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not succ(D,P2,_).

:-  do(action(pushMobKill, D),T), 
    fluent(me(P), T),
    succ(D,P,P2),
    succ(D,P2,P3),
    not fluent(porte(P3, true), T), 
    not fluent(mob(P3),T), 
    not fluent(bloc(P3),T), 
    not fluent(piege(P3,true), T+1),
    not pique(P3),
    not demone(P3).



% effets
fluent(me(P), T):-
    do(action(pushMobKill, D), T-1),
    fluent(me(P), T-1).

removed(mob(P2),T):-
    do(action(pushMobKill, D), T),
    fluent(me(P), T),
    succ(D, P, P2).

%% action moveKey
% preconditions
:-  do(action(moveKey, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(moveKey, D),T), 
    fluent(me(P), T), 
    succ(D, P, P2), 
    fluent(bloc(P2),T).

:-  do(action(moveKey, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    fluent(mob(P2),T).

:-  do(action(moveKey, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not fluent(cle(P2, true),T).

% effets
fluent(me(P2), T):-
    do(action(moveKey, D), T-1),
    succ(D, P,P2),
    fluent(me(P), T-1).

fluent(cle(P2, false), T):-
    do(action(moveKey, D), T-1),
    succ(D, P,P2),
    fluent(me(P), T-1).

removed(cle(P2, S),T):-
    do(action(moveKey, D), T),
    fluent(me(P), T),
    succ(D, P, P2),
    fluent(cle(P2, S), T).

%% action openDoor
% preconditions
:-  do(action(openDoor, D),T), 
    fluent(me(P), T), 
    not succ(D, P, _).

:-  do(action(openDoor, D),T), 
    not fluent(cle(_, false),T).

:-  do(action(openDoor, D),T), 
    fluent(me(P), T),
    succ(D,P,P2), 
    not fluent(porte(P2, true),T).


% effets
fluent(me(P2), T):-
    do(action(openDoor, D), T-1),
    succ(D, P,P2),
    fluent(me(P), T-1).


removed(porte(P2, S),T):-
    do(action(openDoor, D), T),
    fluent(me(P), T),
    succ(D, P, P2),
    fluent(porte(P2, S), T).

% les fluents qui n'ont pas été supprimés restent à leur valeur
fluent(bloc(P), T + 1) :- 
    fluent(bloc(P), T), 
    step(T+1),
    not removed(bloc(P), T).

fluent(mob(P), T + 1) :- 
    fluent(mob(P), T), 
    step(T+1),
    not removed(mob(P), T),
    not fluent(piege(P, true), T+1).

fluent(porte(P, S), T + 1) :- 
    fluent(porte(P, S), T), 
    step(T+1),
    not removed(porte(P, S), T).

fluent(actionRestante(X-1), T):-
    fluent(me(P), T-1),
    not pique(P),
    not fluent(piege(P, true),T-1),
    fluent(actionRestante(X), T-1).

fluent(actionRestante(X-2), T):-
    pique(P),
    fluent(me(P), T-1),
    fluent(actionRestante(X), T-1).

fluent(actionRestante(X-2), T):-
    fluent(piege(P, true),T-1),
    fluent(me(P), T-1),
    fluent(actionRestante(X), T-1).

fluent(cle(P, S), T + 1) :- 
    fluent(cle(P, S), T), 
    step(T+1),
    not removed(cle(P, S), T).

#show do/2.
#show fluent/2.

pique(pos(-1,-1)).