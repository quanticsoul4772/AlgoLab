# AST (etat implemente)

Ce document decrit la representation syntaxique actuellement utilisee par AlgoLab.

## 1. Choix actuel

AlgoLab utilise directement l arbre Lark (`lark.Tree`) produit par le parser.

- Pas de couche AST objet custom active.
- Le fichier `src/algolab/ast_nodes.py` est un placeholder (non utilise en runtime).
- L interpretation se fait via des methodes `visit_<regle>` dans `src/algolab/interpreter.py`.

## 2. Structure generale du Tree

Le noeud racine est `programme`.

Organisation typique :

- `programme`
	- `preamble` (fonctions + declarations globales)
	- `instructions` (bloc principal `DEBUT ... FIN`)

Noeuds importants visites par l interpreteur :

- `fonction`, `declaration`, `affectation`
- `si`, `tant_que`, `pour`
- `lire`, `ecrire`, `appel_fonction`
- `expression`, `expression_arithmetique`, `expression_booleenne`
- `array_access`, `type`, `booleen`, `chaine`, `nombre`

## 3. Correspondance grammaire -> execution

- La grammaire est definie dans `src/algolab/grammar.lark`.
- Chaque regle importante est geree dans l interpreteur par une methode dediee.
- Les tokens et sous-arbres sont resolus dynamiquement (pas de classes de noeuds Python dediees).

## 4. Avantages de l approche actuelle

- Implementation rapide et lisible.
- Moins de code de transformation.
- Facile a faire evoluer tant que la grammaire reste simple.

## 5. Limites connues

- Le couplage grammaire/interpreteur est plus fort.
- Les invariants semantiques sont disperses entre parser, interpreteur et environnement.
- La navigation est moins explicite qu avec une hierarchie de classes AST.

## 6. Evolution possible

Si le langage grossit, une etape de transformation vers un AST objet pourra etre introduite :

1. transformer `Tree` Lark vers des noeuds Python,
2. centraliser validations/invariants sur ces noeuds,
3. decoupler davantage parser et moteur d execution.

Ce choix n est pas necessaire pour le MVP actuel, mais reste une piste d evolution.

