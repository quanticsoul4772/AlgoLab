# Grammaire AlgoLab (version implémentée)

Ce document décrit la grammaire réellement utilisée par le parseur Lark du projet.

## 1. Structure globale du programme

Un programme AlgoLab suit cette structure :

```ebnf
programme: preamble DEBUT instructions FIN
preamble: (fonction | declaration)*
```

- `preamble` contient les déclarations globales et les définitions de fonctions.
- Le bloc principal est encadré par `DEBUT ... FIN`.

## 2. Fonctions

```ebnf
fonction: FONCTION IDENTIFIER "(" params? ")" ":" type instructions RETOURNER expression FIN_FONCTION

params: param_group (("," | ";") param_group)*
param_group: identifiers ":" type
```

- Les paramètres peuvent être séparés par `,` ou `;`.
- Une fonction se termine par `RETOURNER expression` puis `FIN_FONCTION`.

## 3. Déclarations et types

```ebnf
declaration: VARIABLE decl_list
decl_list: decl_group (";" decl_group)*
decl_group: identifiers ":" type
identifiers: IDENTIFIER ("," IDENTIFIER)*

type: TYPE array_spec?
array_spec: "[" INT "]"
```

- Les types supportés par le token `TYPE` : `ENTIER`, `REEL`, `CARACTERE`, `BOOLEEN`, `CHAINE`.
- Les tableaux sont déclarés avec une taille fixe : `Entier[10]`.

## 4. Instructions

```ebnf
instructions: instruction*

instruction: affectation
		   | si
		   | tant_que
		   | pour
		   | lire
		   | ecrire
		   | appel_fonction
```

### 4.1 Affectation

```ebnf
affectation: assignable ASSIGN expression
assignable: IDENTIFIER | array_access
```

Opérateur d’affectation : `<-`.

### 4.2 Conditionnelles

```ebnf
si: SI expression_booleenne ALORS instructions
	(SINON_SI expression_booleenne ALORS instructions)*
	(SINON instructions)?
	FIN_SI
```

### 4.3 Boucles

```ebnf
tant_que: TANT_QUE expression_booleenne FAIRE instructions FIN_TANT_QUE

pour: POUR IDENTIFIER DE expression A expression (PAS expression)? FAIRE instructions FIN_POUR
```

### 4.4 Entrées / sorties

```ebnf
lire: LIRE lire_args
lire_args: assignable | "(" assignable ")"

ecrire: ECRIRE ecrire_args
ecrire_args: expression ("," expression)*
		  | "(" expression ("," expression)* ")"
```

## 5. Expressions

```ebnf
expression: expression_arithmetique
		  | expression_booleenne
		  | chaine
```

### 5.1 Booléen

```ebnf
expression_booleenne: expression_arithmetique comparateur expression_arithmetique
					| expression_booleenne logique expression_booleenne
					| NON expression_booleenne
					| booleen

comparateur: COMP
logique: ET | OU
```

Comparateurs (`COMP`) : `==`, `!=`, `<=`, `>=`, `<`, `>`.

### 5.2 Arithmétique

```ebnf
expression_arithmetique: terme ((PLUS | MINUS) terme)*
terme: facteur ((TIMES | DIV | MOD) facteur)*

facteur: nombre
	   | array_access
	   | IDENTIFIER
	   | appel_fonction
	   | "(" expression_arithmetique ")"

array_access: IDENTIFIER "[" expression_arithmetique "]"
```

### 5.3 Littéraux

```ebnf
nombre: FLOAT | INT
booleen: VRAI | FAUX
chaine: STRING
```

## 6. Appels de fonctions

```ebnf
appel_fonction: IDENTIFIER "(" arguments? ")"
arguments: expression ("," expression)*
```

Un appel de fonction peut apparaître comme instruction ou dans une expression.

## 7. Règles lexicales (tokens)

```ebnf
INT: /-?[0-9]+/
FLOAT: /-?[0-9]+\.[0-9]+/
IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
COMP: /==|!=|<=|>=|<|>/

ASSIGN: <-
PLUS: +
MINUS: -
TIMES: *
DIV: /
MOD: %
```

Mots-clés (insensibles à la casse) :

- `DEBUT`, `FIN`, `VARIABLE`
- `SI`, `ALORS`, `SINON`, `SINON_SI`, `FIN_SI`
- `TANT_QUE`, `FAIRE`, `FIN_TANT_QUE`
- `POUR`, `DE`, `A`, `PAS`, `FIN_POUR`
- `LIRE`, `ECRIRE`
- `FONCTION`, `RETOURNER`, `FIN_FONCTION`
- `VRAI`, `FAUX`, `ET`, `OU`, `NON`
- `TYPE` (`ENTIER|REEL|CARACTERE|BOOLEEN|CHAINE`)

Import Lark :

- `STRING` via `%import common.ESCAPED_STRING`
- espaces ignorés via `%import common.WS` et `%ignore WS`

## 8. Conventions importantes

- Les variantes avec ou sans underscore sont acceptées pour certains mots-clés (`FinSi` / `FIN_SI`, `TantQue` / `TANT_QUE`, etc.).
- Les indices de tableaux sont ensuite validés par l’exécution (règles sémantiques dans l’environnement).
- Cette documentation est alignée sur la source de vérité : `src/algolab/grammar.lark`.
