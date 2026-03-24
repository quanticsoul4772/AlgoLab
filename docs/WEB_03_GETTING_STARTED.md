# Getting started (contenu de page documentation)

## Ce que vous allez faire

En moins de 5 minutes, vous allez :

1. verifier votre installation,
2. executer un premier fichier `.algo`,
3. voir un resultat concret.

## Prerequis

- AlgoLab installe (binaire ou via Python).
- Un terminal (PowerShell, Terminal macOS, bash Linux).

## Etape 1 - Verification rapide

```bash
algolab --help
```

Si une aide s'affiche, vous etes pret.

## Etape 2 - Creer un premier fichier

Creez `hello.algo` avec :

```text
Variable x : Entier
Debut
  x <- 5
  Ecrire x
Fin
```

## Etape 3 - Executer

```bash
algolab hello.algo
```

Sortie attendue :

```text
5
```

## Etape 4 - Essayer du code inline

```bash
algolab -c "Variable x : Entier Debut x <- 3 Ecrire x Fin"
```

## En cas d'erreur

- `command not found` : AlgoLab n'est pas dans le `PATH`.
- `Fichier introuvable` : verifiez le nom et le dossier courant.
- Erreur syntaxique : relisez la structure `Variable ... Debut ... Fin`.

## Suite recommandee

- Installer l'extension VS Code (`.vsix`)
- Activer les diagnostics sur sauvegarde
- Explorer les exemples du dossier `examples/`
