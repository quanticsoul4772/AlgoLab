# Modeles de pages reutilisables

Ce document propose des templates markdown reutilisables pour accelerer la production de contenu web.

## 1) Modele de page tutoriel

~~~md
# Titre de la page

## Objectif
- Ce que l'utilisateur saura faire a la fin.

## Prerequis
- Outil / version / fichiers necessaires.

## Etapes
### 1) Etape
Commande ou action.

### 2) Etape
Commande ou action.

## Verification
Resultat attendu.

## Erreurs courantes
- Erreur A -> solution
- Erreur B -> solution

## Prochaine etape
Lien vers la page suivante.
~~~

## 2) Modele de page reference commande

~~~md
# Nom de la commande

## Syntaxe
```bash
commande [options] [arguments]
```

## Description
Role de la commande.

## Options
- `-x` : description
- `--long` : description

## Exemples
```bash
commande exemple
```

## Retour / codes d'erreur
- `0` : succes
- `1` : erreur
~~~

## 3) Modele de changelog release

~~~md
# vX.Y.Z - YYYY-MM-DD

## Nouveautes
- ...

## Ameliorations
- ...

## Corrections
- ...

## Assets
- linux .deb
- windows .exe
- macOS binaire
- vscode .vsix

## Notes de migration
- ...
~~~

## 4) Modele de page FAQ

~~~md
# FAQ

## Installation
### Q: ...
R: ...

## Utilisation
### Q: ...
R: ...

## Depannage
### Q: ...
R: ...
~~~

## 5) Snippets de CTA

- "Telecharger la derniere release"
- "Installer l'extension VS Code"
- "Lancer mon premier programme"
- "Voir la documentation complete"
