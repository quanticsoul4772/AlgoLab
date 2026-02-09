# Structure proposee pour AlgoLab

## 1. Objectif
AlgoLab est un interpreteur pedagogique d un pseudo code avec une grammaire definie sous Lark. Le coeur est compose d un lexer, d un parser, d un AST et d un interpreteur, avec un systeme d erreurs clair.

## 2. Organisation generale
L organisation suivante regroupe le code, la documentation et les tests pour rester lisible et evolutif.

```
AlgoLab/
├── README.md
├── docs/
│   ├── 01_vision_et_scopes.md
│   ├── 02_grammaire.md
│   ├── 03_ast.md
│   ├── 04_architecture_interpreteur.md
│   ├── 05_memoire_et_types.md
│   └── 06_diagnostics.md
├── src/
│   └── algolab/
│       ├── __init__.py
│       ├── lexer.py
│       ├── parser.py
│       ├── ast_nodes.py
│       ├── interpreter.py
│       ├── environment.py
│       ├── errors.py
│       └── main.py
├── examples/
│   ├── hello_world.algo
│   ├── conditions.algo
│   ├── boucles.algo
│   └── fonctions.algo
└── tests/
    ├── test_lexer.py
    ├── test_parser.py
    ├── test_interpreter.py
    ├── test_types.py
    └── test_errors.py
```

## 3. Correspondance avec les modules existants
La documentation actuelle decrit deja les modules suivants, proposes ici sous src/algolab:

- lexer.py: generation des tokens via la grammaire Lark.
- parser.py: construction de l AST a partir des tokens.
- ast_nodes.py: classes de noeuds ou documentation de la structure AST.
- interpreter.py: visite des noeuds et execution.
- environment.py: gestion des portees et variables.
- errors.py: exceptions et messages pedagogiques.
- main.py: point d entree.

## 4. Documentation
Le fichier existant peut etre place dans docs/05_memoire_et_types.md.
La documentation est separee en chapitres courts pour faciliter la navigation.

- 01_vision_et_scopes.md: objectifs du langage et perimetre.
- 02_grammaire.md: specification EBNF et mots cles.
- 03_ast.md: description de l AST et transformation.
- 04_architecture_interpreteur.md: modules et flux.
- 05_memoire_et_types.md: pile d environnements et types.
- 06_diagnostics.md: erreurs, format des messages, exemples.

## 5. Conventions et choix techniques
- Noms de fichiers en snake_case.
- Un seul point d entree dans main.py.
- Regles de typage de base dans interpreter.py ou environment.py.
- Messages d erreurs centralises dans errors.py.

## 6. Etapes minimales de mise en place
1. Deplacer la documentation existante dans docs/.
2. Creer le package src/algolab/ et separer les modules.
3. Ajouter des exemples .algo pour les cas courants.
4. Ajouter des tests unitaires par sous systeme.

## 7. Notes sur les sources
Le document 5. Gestion de la Memoire et des Types alimente directement docs/05_memoire_et_types.md.
