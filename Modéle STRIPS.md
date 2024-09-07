---
title: "Strips"
author: Charles Bricout
geometry: margin=2cm
output: pdf_document
---
# Modéle STRIPS

## Fluents :
- $me(pos(x,y))$ : position du personnage
- $bloc(pos(x,y))$ : position d'un bloc
- $mob(pos(x,y))$ : position d'un mob
- $actionRestant(x)$ : action restante 
- $piege(pos(x,y), etat)$ : position d'un piege dans un etat 
    - etat = true : le piege est levé (unsafe)
    - etat = false : le piege est baissé (safe)
- $porte(pos(x,y), etat)$ : position d'une porte
    - etat = True : ouverte
    - etat = False : fermée
- $cle(pos(x,y),etat)$ : position d'une clé
    -  etat = True : clé sur le sol
    -  etat = False : clé ramassée

## Prédicats :
- $case(pos(x,y))$ : présence d'une case à la position x, y
- $succ(d, pos(x,y), pos(x2,y2))$ : le couple (x2,y2) sont les coordonées de la case dans la direction d de (x,y). La présence d'un successeurs implique donc la présence d'une case en (x2,y2)
- $pique(pos(x,y))$ : présence d'un pique en (x,y)
- $demone(pos(x,y))$ : presence d'une demone ou ange en (x,y).

## Contraintes :
- $piege(P,true)\land mob(P)$ : nous devons verifier que les monstres meurt si ils sont sur un piege ouvert
- Il faudra aussi s'assurer d'enlever le bon nombre de point d'action quand un piege s'active avec notre héro dessus
- Il faut aussi implémenter un switch automatique des pièges


## But :
- $goal(demone(P)\land me(P2) \land succ(D, P2, P))$ : il y a une demone (ou un ange) dans une case adjacente au héro

## La liste des actions :
- Déplacement simple
- Déplacement vers un pique
- Déplacement vers un piege
- Pousser mob sur case
- Pousser mob sur mur
- Pousser mob sur piques
- Pousser mob sur piege ouvert
- Pousser mob sur mob
- Pousser mob sur porte fermée
- Pousser mob sur bloc
- Pousser mob sur demone
- Pousser bloc sur case
- Pousser bloc sur mur 
- Pousser bloc sur bloc
- Pousser bloc sur mob
- Pousser bloc sur demone
- Déplacement sur une clé
- Ouvrir une porte


## Les actions en détail :

### Déplacement simple :

$do(act(move,D), step)$

- Préconditions : 
\begin{gather*}
 	me(P)\land succ(D,P,P2)\land\lnot mob(P2)\land \\  
 	\lnot bloc(P2)\land\lnot piege(P2,false)\land \lnot pique(P2)\land \lnot porte(P2,true)\land \\   \lnot cle(P2,true)\land actionRestant(N)\land  N > 0
\end{gather*}

- Effets :
\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ me(P2)\land \lnot me(P)\end{gather*}

### Déplacement vers un pique:

$do(act(movePique,D), step)$

- Préconditions : 
\begin{gather*}
me(P)\land succ(D,P,P2)\land   
 	\lnot bloc(P2)\land \\ pique(P2)\land  actionRestant(N)\land  N > 1
\end{gather*}

Il ne peut pas y avoir de piège, de mob, de clé ou de porte sur des piques, nous ne testons donc pas leur présence. 

- Effets :
\begin{gather*}actionRestant(N-2)\land \lnot actionRestant(N)\land\\ me(P2)\land \lnot me(P)\end{gather*}

### Déplacement vers un piege:

$do(act(movePiege,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land   
 	\lnot bloc(P2)\land\\ piege(P2,false)\land actionRestant(N)\land N > 1\end{gather*}

Il ne peut y avoir ni pique, ni mob, ni clé, ni porte sur un piege unsafe, c'est donc inutile de tester leur présence.

- Effets :
\begin{gather*}actionRestant(N-2)\land \lnot actionRestant(N)\land\\ me(P2)\land \lnot me(P)\end{gather*}

### Pousser mob sur case:

$do(act(pushMobCase,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land succ(D,P2,P3)\land mob(P2)\land \\\lnot bloc(P3)\land \lnot piege(P3,false)\land\lnot  pique(P3)\land \lnot porte(P3,true) \land\lnot mob(P3) \land\\\lnot demone(P3) \land actionRestant(N)\land  N > 0\end{gather*}
Ici, il n'est pas necessaire de tester la présence de bloc ou de porte en P2 car il n'est pas possible d'avoir un mob ET ces éléments. De plus un mob ne peut pas non plus être sur des piques ou un pieges unsafe.

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ mob(P3)\land\lnot mob(P2)\end{gather*}

### Pousser mob sur mur:

$do(act(pushMobMur,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land \lnot succ(D,P2,P3)\land\\ mob(P2) \land actionRestant(N)\land  N > 0\end{gather*}

Ici nous pouvons simplifier car si il n'y a pas de successeurs, il y a un mur et donc il ne peut rien y avoir d'autre !

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}

### Pousser mob sur piques :

$do(act(pushMobSpike,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land mob(P2)\land\\ pique(P3)\land \lnot bloc(P3) \land actionRestant(N)\land  N > 0\end{gather*}

Nous ne testons pas la présence d'un piège ou d'un mob car ils ne peuvent pas être au même endroit que les piques.

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2) \end{gather*}

### Pousser mob sur piege ouvert:

$do(act(pushMobPiegeO,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land mob(P2)\land\\ piege(P3, false)\land \lnot bloc(P3) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}


### Pousser mob sur mob:

$do(act(pushMobMob,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ mob(P2)\land mob(P3) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}

### Pousser mob sur porte fermée:

$do(act(pushMobDoor,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land mob(P2)\land\\ porte(P3, true) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}

### Pousser mob sur bloc:

$do(act(pushMobBloc,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ mob(P2)\land bloc(P3) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}

### Pousser mob sur demone:

$do(act(pushMobDemone,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ mob(P2)\land demone(P3) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\ \lnot mob(P2)\end{gather*}

### Pousser bloc sur case:

$do(act(pushBlocCase,D), step)$

- Préconditions : 
\begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land bloc(P2)\land \lnot porte(P3, true)\land\\ \lnot bloc(P3)\land\lnot mob(P3) \land \lnot demone(P3) \land actionRestant(N)\land  N > 0\end{gather*}

Nous pouvons tout à fait pousser des blocs sur un pique,un piege ou une clé avec la même action !

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land\\   bloc(P3)\land\lnot bloc(P2)\end{gather*}


### Pousser bloc sur mur:

$do(act(pushBlocMur,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  \lnot succ(D,P2,P3)\land\\ bloc(P2) \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\end{gather*}

### Pousser bloc sur bloc:

$do(act(pushBlocBloc,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ bloc(P2)\land bloc(P3)  \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 		\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\end{gather*}

### Pousser bloc sur mob:

$do(act(pushBlocMob,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ bloc(P2)\land mob(P3)  \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\end{gather*}

### Pousser bloc sur demone:

$do(act(pushBlocMob,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land  succ(D,P2,P3)\land\\ bloc(P2)\land demone(P3)  \land actionRestant(N)\land  N > 0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\end{gather*}

### Déplacement sur une clé:

$do(act(moveKey,D), step)$

- Préconditions : 
 \begin{gather*}me(P)\land succ(D,P,P2)\land \lnot mob(P2)\land 
 	\lnot bloc(P2)\land \\  cle(P2,true)\land actionRestant(N)\land N >0\end{gather*}

- Effets :
 			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land \\ \lnot cle(P2, true) \land cle(P2, false)\land\\ \lnot me(P) \land me(P2)\end{gather*}

### Ouvrir une porte:

$do(act(openDoor,D), step)$

- Préconditions :
 \begin{gather*}me(P)\land succ(D,P,P2)
 	\land cle(P3, false)\land \\  porte(P2,true)\land actionRestant(N)\land N >0\end{gather*}

- Effets :
			\begin{gather*}actionRestant(N-1)\land \lnot actionRestant(N)\land \\ \lnot porte(P2, true) \land porte(P2, false)\land\\ \lnot me(P) \land me(P2)\end{gather*}

