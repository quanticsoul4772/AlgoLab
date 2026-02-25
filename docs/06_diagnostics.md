# Diagnostics (etat implemente)

Ce document decrit le systeme de diagnostics actuellement implemente dans AlgoLab, avec les types d erreurs, le format des messages et les messages guides de syntaxe.

## 1. Classes d erreurs

Le projet utilise une hierarchie simple :

- `AlgoLabError` (classe de base)
- `SyntaxErrorAlgoLab`
- `SemanticErrorAlgoLab`
- `RuntimeErrorAlgoLab`

Implementation : `src/algolab/errors.py`.

## 2. Format des messages

Le format standard est :

`<Prefixe> (Ligne X, Colonne Y) : <message>`

Exemples de prefixes :

- `Erreur Syntaxique`
- `Erreur Semantique`
- `Erreur d execution`

Si la position n est pas disponible, le message reste sans localisation.

## 3. Ou les diagnostics sont produits

### 3.1 Parsing (`src/algolab/parser.py`)

- Les erreurs Lark (`UnexpectedInput`) sont converties en `SyntaxErrorAlgoLab`.
- Le parser conserve la position (`line`, `column`) quand elle est disponible.
- Une chaine de contexte Lark peut etre incluse : `Syntaxe invalide. Contexte: ...`.

### 3.2 Execution (`src/algolab/interpreter.py` + `src/algolab/environment.py`)

- Les erreurs metier (type, variable, index, execution) sont levees en `SemanticErrorAlgoLab` ou `RuntimeErrorAlgoLab`.
- L interpreteur re-propage la ligne/colonne via les metadonnees de noeud Lark si l exception ne contient pas deja de position.

## 4. Diagnostics guides de syntaxe

Le parser implemente plusieurs heuristiques pour fournir un message pedagogique plutot qu une erreur brute Lark :

- `SI ...` sans `ALORS` -> `mot-cle ALORS manquant apres la condition`.
- `TANT_QUE ...` sans `FAIRE` -> `mot-cle FAIRE manquant apres la condition`.
- `POUR ...` sans `FAIRE` -> `mot-cle FAIRE manquant apres l en-tete du POUR`.
- `POUR ... PAS` sans valeur -> `valeur manquante apres PAS. Exemple: PAS 1`.
- `LIRE` sans argument -> `variable attendue apres LIRE`.
- `ECRIRE` sans argument -> `expression attendue apres ECRIRE`.
- Operateur en fin de ligne (`+`, `-`, `*`, `/`, `%`) -> `operande manquante apres operateur`.
- Bloc non ferme (`SI`, `TANT_QUE`, `POUR`) -> `Bloc non ferme: <FIN_...> attendu` avec ligne d ouverture.

## 5. Erreurs semantiques et d execution frequentes

Exemples typiques emis par l environnement/runtime :

- `Variable non declaree: <nom>`
- `Variable non initialisee: <nom>`
- `Type attendu ENTIER|REEL|CARACTERE|BOOLEEN`
- `Index de tableau commence a 1`
- `Index de tableau hors limites`
- `Division par zero`

## 6. Cas verifies par tests

Les diagnostics critiques sont verifies par tests unitaires :

- `tests/test_errors.py`
- `tests/test_edge_cases.py`
- `tests/test_types.py`

Exemples testes :

- format de message avec ligne/colonne,
- variable non declaree,
- messages guides `ALORS`/`FAIRE`/`PAS`,
- index hors bornes.

## 7. Limites actuelles

- Les suggestions de correction sont heuristiques (pas un moteur de reparation complet).
- Certaines erreurs syntaxiques complexes peuvent encore retomber sur un message `Syntaxe invalide` plus generique.
- Le systeme ne propose pas encore de codes d erreur stables (ID), uniquement des messages texte.
