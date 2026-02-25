# Architecture de l interpréteur (état actuel)

Ce document décrit l architecture réellement implémentée dans AlgoLab.

## 1. Vue d ensemble

AlgoLab suit une architecture simple en 3 étapes :

1. **Chargement du code source** (fichier ou inline).
2. **Parsing** avec Lark en arbre syntaxique (`Tree`).
3. **Interprétation** de cet arbre avec gestion d environnement typé.

Le projet privilégie un modèle direct : l interpréteur parcourt l arbre Lark sans couche AST objet custom intermédiaire.

## 2. Flux d exécution

```mermaid
flowchart TD
		A[main.py] --> B[Interpreter.run(source)]
		B --> C[parser.parse_source(source)]
		C --> D[Lark parser + grammar.lark]
		D --> E[Tree Lark]
		E --> F[Interpreter.visit(...)]
		F --> G[Environment]
		F --> H[errors.py]
		F --> I[writer / reader]
```

### Détail opérationnel

- `main.py` lit le code, puis lance `Interpreter().run(source)`.
- `parse_source` construit le parser LALR et retourne un `Tree` Lark.
- `Interpreter` dispatch chaque nœud via `visit_<nom_du_noeud>`.
- `Environment` gère déclaration, affectation, résolution, types et tableaux.
- Les erreurs sont remontées avec classes dédiées et, si possible, ligne/colonne.

## 3. Modules et responsabilités

### 3.1 `src/algolab/main.py`

- Point d entrée CLI.
- Accepte un fichier source ou `--code` inline.
- Attrape les erreurs AlgoLab et renvoie un code de sortie non nul.

### 3.2 `src/algolab/parser.py`

- Construit le parser Lark à partir de `grammar.lark`.
- Expose `get_parser()` et `parse_source(source)`.
- Transforme les erreurs Lark (`UnexpectedInput`) en `SyntaxErrorAlgoLab`.
- Ajoute des heuristiques pédagogiques (ex: `ALORS`/`FAIRE` manquant, `PAS` sans valeur, bloc non fermé).

### 3.3 `src/algolab/grammar.lark`

- Source de vérité syntaxique du langage.
- Définit règles programme, fonctions, instructions, expressions et tokens.
- Les mots-clés sont gérés en mode insensible à la casse.

### 3.4 `src/algolab/interpreter.py`

- Cœur d exécution (visiteur sur arbre Lark).
- Implémente :
	- déclarations et affectations,
	- `SI`, `TANT_QUE`, `POUR`,
	- `LIRE`/`ECRIRE`,
	- fonctions (définition, appel, retour),
	- expressions arithmétiques/logiques,
	- accès tableaux.
- Propage les positions d erreur en ré-emballant les exceptions si nécessaire.

### 3.5 `src/algolab/environment.py`

- Modèle de portée parent/enfant (`Environment(parent=...)`).
- Stocke les variables typées (`TypeSpec`, `Variable`).
- Applique les règles de type (`ENTIER`, `REEL`, `CARACTERE`, `BOOLEEN`).
- Gère les tableaux à taille fixe avec indexation logique 1..N.

### 3.6 `src/algolab/errors.py`

- Définit les exceptions spécialisées :
	- `SyntaxErrorAlgoLab`
	- `SemanticErrorAlgoLab`
	- `RuntimeErrorAlgoLab`
- Standardise le format des messages et la localisation ligne/colonne.

### 3.7 `src/algolab/lexer.py` et `src/algolab/ast_nodes.py`

- **État actuel : placeholders**.
- Le lexer n est pas isolé dans un module dédié : il est implicitement porté par Lark via `grammar.lark`.
- L AST objet custom n est pas utilisé : l interprétation se fait directement sur `Tree`.

## 4. Données et modèle mémoire

Le runtime repose sur deux structures :

- `TypeSpec(base, size)` : type scalaire ou tableau.
- `Environment._values: dict[str, Variable]` : table des symboles typée.

Règles importantes :

- Variable non déclarée -> erreur sémantique.
- Variable scalaire non initialisée lue -> erreur d exécution.
- Affectation directe d un tableau -> interdite.
- Index tableau : entier, >= 1, <= taille.

## 5. I/O et intégration CLI

- Entrées utilisateur : via callback `reader` (défaut `input`).
- Sorties : via callback `writer` (défaut `print`).
- Cela facilite les tests unitaires (injection de reader/writer).

## 6. Qualité et tests (état projet)

- Le socle de tests couvre désormais parser, lexer (via Lark), interpréteur, types et erreurs.
- Les tests utilisent un `conftest.py` pour injecter `src` dans `PYTHONPATH` de test.

## 7. Limites connues

- Pas de séparation lexer/parser custom hors Lark.
- Pas de couche AST orientée objets (classes de nœuds dédiées).
- Documentation historique encore incomplète sur certains chapitres (hors ce fichier mis à jour).

## 8. Évolutions recommandées

1. Choisir explicitement une stratégie AST : conserver `Tree` ou introduire un transformer objet.
2. Documenter les invariants d exécution (types, scopes, indexation) dans un guide de contribution.
3. Enrichir les tests de non-régression avec jeux d exemples `examples/*.algo`.
