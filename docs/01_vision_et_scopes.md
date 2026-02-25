# Vision et scopes (etat courant)

Ce document formalise la vision d AlgoLab et le perimetre reel du projet a la date actuelle.

## 1. Vision

AlgoLab est un interpreteur pedagogique de pseudo-code, pense pour l apprentissage de l algorithmique.

Objectifs principaux :

- proposer une syntaxe lisible et proche du cours (DEBUT/FIN, SI, POUR, etc.),
- executer les programmes de maniere deterministe,
- fournir des messages d erreurs comprehensibles,
- rester simple a maintenir pour un usage educatif.

## 2. Public cible

- apprenants debutants en algorithmique,
- enseignants souhaitant illustrer des notions de base,
- developpeurs qui veulent un mini-langage de demonstration.

## 3. Perimetre fonctionnel (in-scope)

Le projet couvre actuellement :

- declarations typees (`ENTIER`, `REEL`, `CARACTERE`, `BOOLEEN`, `CHAINE`),
- affectations et expressions arithmetiques/logiques,
- structures de controle (`SI`, `SINON_SI`, `SINON`, `TANT_QUE`, `POUR`),
- entrees/sorties (`LIRE`, `ECRIRE`),
- fonctions (definition, appel, retour),
- tableaux a taille fixe,
- diagnostics syntaxiques/semantiques/execution.

## 4. Hors perimetre actuel (out-of-scope)

Fonctionnalites non prises en charge dans l etat actuel :

- moteur de compilation (AlgoLab est un interpreteur),
- systeme de modules/imports,
- objets/classes,
- optimisation avancee,
- IDE interne ou interface graphique dediee.

## 5. Principes de conception

- **Source de verite syntaxique** : `src/algolab/grammar.lark`.
- **Execution simple** : parcours direct de l arbre Lark (`Tree`) sans AST objet intermediaire.
- **Pedagogie avant complexite** : erreurs explicites et heuristiques de correction.
- **Maintenabilite** : separation claire parser / runtime / environnement / erreurs.

## 6. Etat de maturite

Le coeur interpreter est fonctionnel (MVP solide) :

- exemples `.algo` executables,
- suite de tests active (`24 passed` au dernier etat),
- documentation technique des composants principaux mise a jour.

## 7. Prochaines priorites

1. stabiliser et etendre les tests de non-regression,
2. enrichir les docs de contribution developpeur,
3. clarifier la strategie AST long terme (Lark direct vs AST objet),
4. ajouter davantage de cas pedagogiques dans `examples/`.

