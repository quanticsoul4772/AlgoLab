# Gestion de la memoire et des types (etat implemente)

Ce document decrit le comportement reel de la memoire d execution et des regles de types dans AlgoLab.

## 1. Modele memoire

Le runtime s appuie sur `Environment` (`src/algolab/environment.py`) avec une table de symboles typee.

Structures principales :

- `TypeSpec(base, size)`
  - `base` : type scalaire (`ENTIER`, `REEL`, `CARACTERE`, `BOOLEEN`)
  - `size` : taille du tableau si non nul
- `Variable(type_spec, value)`
- `Environment._values: dict[str, Variable]`

Chaque environnement peut pointer vers un parent, ce qui permet la resolution de portees.

## 2. Portee et resolution

Regles appliquees :

- declaration interdite en doublon dans le meme environnement,
- resolution d un identifiant : scope courant puis chainage parent,
- erreur semantique si variable non declaree,
- erreur d execution si variable scalaire lue avant initialisation.

Fonctions :

- un appel de fonction cree un environnement local enfant,
- les parametres sont declares et affectes dans ce scope local,
- la sortie de fonction restaure l environnement precedent.

## 3. Types supportes et coercions

Types pris en charge en execution :

- `ENTIER`
- `REEL`
- `CARACTERE`
- `BOOLEEN`

Note implementation : le token de grammaire accepte aussi `CHAINE`, mappe en runtime vers `CARACTERE`.

Regles de coercion (runtime actuel) :

- `ENTIER <- ENTIER` : accepte
- `ENTIER <- REEL` : rejete (`Type attendu ENTIER`)
- `REEL <- ENTIER` : accepte (coercion vers float)
- `REEL <- REEL` : accepte
- `CARACTERE <- str` : accepte
- `BOOLEEN <- bool` : accepte

## 4. Tableaux

Les tableaux sont a taille fixe :

- declaration via `TypeSpec(..., size=n)`,
- stockage interne : liste Python de longueur `n`, initialisee a `None`.

Contraintes :

- l affectation directe d un tableau complet est interdite,
- indexation reservee aux variables tableau,
- index attendu entier,
- index logique de 1 a `n` (pas 0-based expose a l utilisateur).

Erreurs associees :

- `Index de tableau doit etre un entier`
- `Index de tableau commence a 1`
- `Index de tableau hors limites`
- `Variable non initialisee: nom[index]`

## 5. Entrees / sorties et types

`LIRE` convertit la saisie selon le type de la variable cible :

- `ENTIER` -> `int`
- `REEL` -> `float`
- `CARACTERE` -> `str`
- `BOOLEEN` -> `VRAI` / `FAUX`

En cas d entree invalide, une erreur semantique explicite est levee.

## 6. Cas limites verifies par tests

Couverts dans `tests/test_edge_cases.py` et modules associes :

- types mixtes (`ENTIER + REEL`),
- rejet de `REEL -> ENTIER`,
- appels de fonctions en chaine,
- recursion (factorielle),
- ecritures/lectures hors bornes tableau,
- variables non initialisees,
- variables non declarees.

## 7. Limites actuelles

- pas de conversion explicite utilisateur (`cast`) dans le langage,
- pas de types structures (objets, enregistrements),
- pas de tableaux multidimensionnels,
- pas de verification statique separee (controle principalement au runtime).

## 8. References code

- `src/algolab/environment.py`
- `src/algolab/interpreter.py`
- `src/algolab/grammar.lark`
- `tests/test_types.py`
- `tests/test_edge_cases.py`
