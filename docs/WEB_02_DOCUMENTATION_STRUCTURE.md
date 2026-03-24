# Structure recommandee de la documentation

Ce document definit l'arborescence de la future doc publique.

## 1) Navigation principale

### Demarrer

- Introduction
- Installation
- Premier programme

### Utiliser AlgoLab

- Executer un fichier
- Executer du code inline
- Entrees/sorties (`LIRE`, `ECRIRE`)
- Types et variables

### VS Code

- Installation de l'extension
- Bouton Run
- Verification et diagnostics
- Parametres de l'extension

### Reference

- Syntaxe du langage
- Instructions de controle
- Fonctions
- Tableaux
- Erreurs et diagnostics

### Support

- FAQ
- Depannage installation
- Signaler un bug

## 2) Arborescence de fichiers markdown

```text
docs/
  WEB_00_PLAN_GLOBAL.md
  WEB_01_LANDING_PAGE_COPY.md
  WEB_02_DOCUMENTATION_STRUCTURE.md
  WEB_03_GETTING_STARTED.md
  WEB_04_INSTALLATION_MULTI_OS.md
  WEB_05_PAGE_EXTENSION_VSCODE.md
  WEB_06_FAQ_TROUBLESHOOTING.md
  WEB_07_MODELES_PAGES.md
```

## 3) Standard de chaque page doc

Chaque page doit contenir :

1. Ce que l'utilisateur va apprendre
2. Prerequis
3. Etapes pas a pas
4. Exemple minimal executable
5. Resultat attendu
6. Erreurs frequentes
7. Prochaine etape recommandee

## 4) Liens transverses obligatoires

Chaque page doit proposer :

- lien vers installation,
- lien vers FAQ,
- lien vers releases.

## 5) Niveau de detail par audience

### Debutant

- Plus de captures et commandes copier-coller.
- Explications explicites sur PATH, terminal, extensions.

### Enseignant

- Section "deploiement classe" (postes heterogenes, checklists).
- Scenarios de TP rapides.

### Avance

- Liens vers docs techniques existantes (`docs/01_vision_et_scopes.md`, etc.).

## 6) Qualite editoriale

- Un seul sujet par page.
- Exemples verifiables.
- Pas de blocs de texte trop longs.
- Noms de commandes en monospace.

## 7) Indicateurs de qualite documentaire

- Temps pour premier succes < 10 minutes.
- Taux d'erreur d'installation reduit (feedback support).
- FAQ couvre les 10 erreurs les plus frequentes.
