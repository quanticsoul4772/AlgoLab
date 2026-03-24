# Plan global du site AlgoLab

Ce document sert de point d'entree pour construire :

- la landing page,
- la documentation utilisateur,
- la documentation enseignant,
- la base de contenu support/FAQ.

## 1) Objectif business et produit

AlgoLab doit se positionner comme :

- un outil pedagogique simple pour apprendre l'algorithmique,
- un moteur executable multi-plateforme (Linux, macOS, Windows),
- une extension VS Code pratique pour coder, verifier et executer.

Objectifs du site :

1. Expliquer la proposition de valeur en moins de 10 secondes.
2. Permettre l'installation en moins de 5 minutes.
3. Rassurer sur la stabilite et la compatibilite multi-OS.
4. Donner un chemin clair pour debutants et enseignants.

## 2) Personas cibles

### Etudiant debutant

- Besoin : ecrire un premier programme rapidement.
- Peurs : erreur d'installation, syntaxe incomprise.
- Message cle : "Tu installes, tu lances, tu comprends tes erreurs."

### Enseignant / formateur

- Besoin : environnement stable pour une classe.
- Peurs : heterogeneite des machines, perte de temps en support.
- Message cle : "Meme moteur sur les 3 OS + doc claire + extension VS Code."

### Auto-apprenant

- Besoin : tutoriels concrets, progression pas a pas.
- Message cle : "Guide de demarrage + exemples + FAQ."

## 3) Architecture des pages recommandee

1. Landing page (`/`)
2. Getting started (`/docs/getting-started`)
3. Installation (`/docs/installation`)
4. Utilisation CLI (`/docs/cli`)
5. Extension VS Code (`/docs/vscode`)
6. Erreurs et diagnostics (`/docs/diagnostics`)
7. FAQ (`/docs/faq`)
8. Changelog / releases (`/docs/releases`)

## 4) Parcours utilisateur prioritaire

### Parcours A : "Je veux essayer maintenant"

Landing -> bouton "Installer" -> installation OS -> premier programme -> succes.

### Parcours B : "Je veux integrer en cours"

Landing -> section enseignants -> installation standardisee -> extension VS Code -> FAQ support.

## 5) Messages principaux a repeter

- "Stable v1 multi-plateforme"
- "Executable sur Linux, macOS, Windows"
- "Extension VS Code avec execution et diagnostics"
- "Pensee pour l'apprentissage"

## 6) Calls-to-action (CTA)

CTA primaires :

- "Telecharger la derniere release"
- "Commencer en 5 minutes"

CTA secondaires :

- "Installer l'extension VS Code"
- "Voir les exemples"
- "Lire la FAQ"

## 7) Checklist de publication

- [ ] Page d'accueil avec CTA visibles sans scroll.
- [ ] Liens directs vers assets release (`.deb`, `.exe`, binaire macOS, `.vsix`).
- [ ] Guide d'installation par OS.
- [ ] Exemples de commandes copier-coller.
- [ ] Captures d'ecran extension VS Code.
- [ ] FAQ erreurs courantes.
- [ ] Changelog versionne.

## 8) Convention editoriale

- Ton : simple, pedagogique, orientee action.
- Phrases courtes, exemples concrets.
- Eviter le jargon interne.
- Toujours fournir une commande test de verification.

## 9) Definition de "pret a publier"

Le site est "pret" quand un utilisateur inconnu peut :

1. installer AlgoLab sur son OS,
2. executer `hello_world.algo`,
3. installer l'extension VS Code,
4. corriger une erreur grace aux diagnostics,
5. trouver de l'aide via la FAQ.
