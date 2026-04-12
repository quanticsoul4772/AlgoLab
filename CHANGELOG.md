# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), et ce projet adhère au [Versionnement Sémantique](https://semver.org/lang/fr/).

## [Unreleased]

### Ajouté
- Fichiers communautaires open source (README, CONTRIBUTING, CODE_OF_CONDUCT, templates d'issues/PR)
- Licence MIT

---

## [0.1.0] - 2024

### Ajouté
- Interpréteur de pseudo-code fonctionnel basé sur Lark
- Grammaire complète : variables typées (`Entier`, `Reel`, `Caractere`, `Booleen`, `Chaine`), tableaux
- Structures de contrôle : `Si/SinonSi/Sinon/FinSi`, `Pour/FinPour`, `TantQue/FinTantQue`
- Fonctions avec paramètres typés et `Retourner`
- Entrées/sorties : `Lire`, `Ecrire`
- Système d'erreurs pédagogiques (syntaxe, sémantique, exécution)
- CLI : exécution de fichiers `.algo` et code inline (`-c`)
- Extension VS Code : coloration syntaxique, snippets, exécution intégrée
- CI/CD GitHub Actions : tests, linting, build multi-OS (Linux .deb, Windows .exe, macOS)
- 13 exemples de programmes dans `examples/`
- Suite de tests (24 tests)
- Documentation technique dans `docs/`

[Unreleased]: https://github.com/adandeigor/AlgoLab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/adandeigor/AlgoLab/releases/tag/v0.1.0
