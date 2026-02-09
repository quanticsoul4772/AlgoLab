# Gestion de la Memoire et des Types

### 2.3. Mots-cles Reserves

Les mots-cles suivants sont reserves et ne peuvent pas etre utilises comme identifiants de variables ou de fonctions :
`DEBUT`, `FIN`, `VARIABLE`, `ENTIER`, `REEL`, `CARACTERE`, `BOOLEEN`, `SI`, `ALORS`, `SINON`, `FIN_SI`, `TANT_QUE`, `FAIRE`, `FIN_TANT_QUE`, `POUR`, `DE`, `A`, `PAS`, `FIN_POUR`, `LIRE`, `ECRIRE`, `VRAI`, `FAUX`, `ET`, `OU`, `NON`.

## 3. Structure de l Arbre Syntaxique Abstrait (AST)

L AST est une representation hierarchique du programme source, depouillee des details syntaxiques non essentiels. Lark generera automatiquement cet AST, que l interpreteur parcourra pour executer le code. Chaque noeud de l AST correspondra a une construction logique du langage.

### 3.1. Exemples de Noeuds AST

*   **`programme`** : Noeud racine, contient une liste d instructions.
*   **`declaration_variable`** : Contient l identifiant de la variable et son type.
*   **`affectation`** : Contient l identifiant de la variable cible et l expression a affecter.
*   **`si_alors_sinon`** : Contient l expression booleenne de la condition, une liste d instructions pour le bloc `ALORS`, et optionnellement une liste d instructions pour le bloc `SINON`.
*   **`tant_que`** : Contient l expression booleenne de la condition et une liste d instructions pour le corps de la boucle.
*   **`pour`** : Contient l identifiant de la variable d iteration, l expression de debut, l expression de fin, l expression du pas (optionnel), et une liste d instructions pour le corps de la boucle.
*   **`lire`** : Contient l identifiant de la variable ou stocker la valeur lue.
*   **`ecrire`** : Contient l expression ou la chaine de caracteres a afficher.
*   **`appel_fonction`** : Contient l identifiant de la fonction et une liste d expressions pour les arguments.
*   **`expression_booleenne`** : Represente une expression logique (comparaison, `ET`, `OU`, `NON`).
*   **`expression_arithmetique`** : Represente une expression mathematique (`+`, `-`, `*`, `/`).
*   **`_IDENTIFIER`**, **`_NUMBER`**, **`_STRING`** : Noeuds terminaux representant les valeurs litterales ou les references.

### 3.2. Transformation de l AST (Optionnel : Transformer Lark)

Pour simplifier l interpretation, il pourra etre utile d utiliser la fonctionnalite `Transformer` de Lark. Cela permet de parcourir l AST genere par le parser et de le transformer en une structure plus optimisee ou plus facile a manipuler pour l interpreteur. Par exemple, on pourrait convertir les noeuds de l AST en objets Python specifiques representant chaque type d instruction ou d expression.

## 4. Architecture Logicielle de l Interpreteur

L interpreteur AlgoLab sera structure en plusieurs modules Python, chacun ayant une responsabilite claire.

### 4.1. Vue d Ensemble des Modules

```mermaid
graph TD
    A[Code Pseudo-code] --> B(Lexer - Lark)
    B --> C(Parser - Lark)
    C --> D[Arbre Syntaxique Abstrait (AST)]
    D --> E(Interpreteur/Executeur)
    E --> F[Environnement d Execution (Variables, Fonctions)]
    E --> G[Gestionnaire d Erreurs Pedagogiques]
    F --> E
    G --> H[Messages d Erreurs Utilisateur]
    E --> I[Sortie (ECRIRE, Resultats)]
```

### 4.2. Description Detaillee des Modules

1.  **`algolab_lexer.py` (via Lark)** :
    *   **Role** : Convertir le texte source en une sequence de tokens.
    *   **Implementation** : Utilisation de la grammaire EBNF definie dans Lark pour generer le lexer. Gere les espaces blancs et les retours a la ligne.

2.  **`algolab_parser.py` (via Lark)** :
    *   **Role** : Verifier la conformite syntaxique des tokens et construire l AST.
    *   **Implementation** : Utilisation de la grammaire EBNF de Lark pour generer le parser. En cas d erreur syntaxique, Lark leve une exception qui sera interceptee par le gestionnaire d erreurs.

3.  **`algolab_ast.py`** :
    *   **Role** : Definir les classes de noeuds de l AST si une transformation manuelle est effectuee, ou servir de documentation pour la structure de l AST generee par Lark.
    *   **Implementation** : Peut contenir des classes Python pour chaque type de noeud AST, facilitant l interpretation.

4.  **`algolab_interpreter.py`** :
    *   **Role** : Parcourir l AST et executer les instructions du programme.
    *   **Implementation** : Une classe `Interpreter` avec une methode `visit(node)` qui dispatchera l execution en fonction du type de noeud AST. Utilise un `Environment` pour gerer les variables.

5.  **`algolab_environment.py`** :
    *   **Role** : Gerer la portee des variables (locale, globale) et stocker leurs valeurs.
    *   **Implementation** : Une classe `Environment` qui maintient un dictionnaire de variables pour la portee courante et un lien vers la portee parente (pour les fonctions et les blocs de code).

6.  **`algolab_errors.py`** :
    *   **Role** : Definir les classes d exceptions specifiques a AlgoLab et formuler des messages d erreurs pedagogiques.
    *   **Implementation** : Classes comme `SyntaxErrorAlgoLab`, `SemanticErrorAlgoLab`, `RuntimeErrorAlgoLab`. Chaque exception contiendra des informations contextuelles (ligne, colonne, nature de l erreur) pour generer un message clair.

7.  **`algolab_main.py`** :
    *   **Role** : Point d entree de l application. Gere la lecture du fichier source, l appel au lexer parser interpreteur, et l affichage des resultats ou des erreurs.
    *   **Implementation** : Fonction principale qui orchestre l ensemble du processus.

## 5. Gestion de la Memoire et des Types

### 5.1. Environnement d Execution

L interpreteur maintiendra une pile d environnements (`Environment` objects). Chaque fois qu un nouveau bloc de code avec sa propre portee est entre (par exemple, une fonction, un bloc `SI`, `TANT_QUE`, `POUR`), un nouvel environnement sera cree et empile. Les variables seront recherchees d abord dans l environnement courant, puis dans les environnements parents successifs.

### 5.2. Types de Donnees

AlgoLab supportera les types de donnees suivants, avec une verification de type basique lors de l affectation et des operations :

*   **`ENTIER`** : Nombres entiers (ex: `10`, `-5`).
*   **`REEL`** : Nombres a virgule flottante (ex: `3.14`, `-0.5`).
*   **`CARACTERE`** : Chaines de caracteres (ex: "Bonjour", 'a').
*   **`BOOLEEN`** : Valeurs logiques (`VRAI`, `FAUX`).

Les conversions de type implicites seront limitees pour eviter la confusion. Par exemple, l affectation d un `REEL` a un `ENTIER` devrait generer une erreur semantique ou un avertissement, a moins d une conversion explicite (non prevue dans cette version initiale pour simplifier).

## 6. Systeme de Diagnostic et Messages d Erreurs Pedagogiques

Un aspect crucial d AlgoLab est sa capacite a fournir des retours constructifs aux apprenants. Le systeme de diagnostic sera concu pour intercepter les erreurs a differents niveaux (lexical, syntaxique, semantique, execution) et les traduire en messages comprehensibles.

### 6.1. Types d Erreurs

*   **Erreurs Lexicales** : Caracteres non reconnus.
*   **Erreurs Syntaxiques** : Non-conformite a la grammaire du langage (ex: mot-cle manquant, structure incorrecte).
*   **Erreurs Semantiques** : Problemes de logique qui ne sont pas des erreurs syntaxiques (ex: variable non declaree, operation sur types incompatibles).
*   **Erreurs d Execution** : Problemes survenant pendant l execution (ex: division par zero, indice hors limites).

### 6.2. Format des Messages d Erreurs

Chaque message d erreur inclura :
*   **Type d erreur** : (Ex: Erreur Syntaxique, Erreur Semantique).
*   **Localisation** : Numero de ligne et de colonne ou l erreur a ete detectee.
*   **Description claire** : Explication de l erreur en termes simples, evitant le jargon technique.
*   **Suggestion de correction** : Si possible, une indication sur la maniere de resoudre le probleme.

**Exemples de messages d erreurs pedagogiques :**

*   **Code** : `DEBUT\n  VARIABLE x : ENTIER\n  x <- 10\n  SI x > 5 ALORS\n    ECRIRE "x est grand"\n  FIN_SI\n  FIN_PROG`
*   **Erreur** : `Erreur Syntaxique (Ligne 7, Colonne 7) : Mot-cle inattendu 'FIN_PROG'. Attendait 'FIN'.`
*   **Suggestion** : `Verifiez que tous les blocs (DEBUT/FIN, SI/FIN_SI, TANT_QUE/FIN_TANT_QUE, POUR/FIN_POUR) sont correctement fermes avec le mot-cle approprie.`

*   **Code** : `DEBUT\n  y <- 5\n  FIN`
*   **Erreur** : `Erreur Semantique (Ligne 2, Colonne 3) : Variable 'y' non declaree avant utilisation.`
*   **Suggestion** : `Declarez la variable 'y' avec le mot-cle 'VARIABLE' et son type avant de l utiliser (ex: VARIABLE y : ENTIER).`

## 7. References

[1] Lark Parsing Toolkit. (n.d.). *Documentation officielle*. [Lien](https://lark-parser.readthedocs.io/en/latest/)
[2] Python Software Foundation. (n.d.). *Documentation Python*. [Lien](https://docs.python.org/3/)
[3] Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools (2nd ed.)*. Addison-Wesley. (Reference generale sur la conception de compilateurs et interpreteurs)
