# Extension VS Code - contenu de page documentation

## Pourquoi utiliser l'extension

L'extension AlgoLab apporte une experience plus confortable :

- coloration syntaxique,
- snippets de structure,
- bouton Run,
- verification et diagnostics dans "Problems".

## Installation de l'extension

1. Telechargez `algolab-vscode.vsix` depuis la derniere release.
2. Ouvrez VS Code.
3. Extensions -> menu `...` -> **Install from VSIX...**
4. Selectionnez le fichier `.vsix`.

## Commandes disponibles

- **Exécuter AlgoLab** (`algolab.run`)
- **Vérifier AlgoLab** (`algolab.validate`)

## Fonctionnement des diagnostics

- A la sauvegarde, l'extension peut lancer une validation automatique.
- En cas d'erreur, un diagnostic est cree avec message et position.
- Les erreurs apparaissent dans le panneau **Problems**.

## Parametres de configuration

### `algolab.executablePath`

Chemin de la commande AlgoLab (par defaut `algolab`).

### `algolab.diagnosticsOnSave`

Active ou desactive la verification automatique lors de la sauvegarde.

### `algolab.diagnosticsTimeoutMs`

Duree maximale de verification en millisecondes.

## Exemple de settings.json

```json
{
  "algolab.executablePath": "algolab",
  "algolab.diagnosticsOnSave": true,
  "algolab.diagnosticsTimeoutMs": 3000
}
```

## Bonnes pratiques pour la classe

- Installer le meme `.vsix` sur toutes les machines.
- Utiliser un meme dossier d'exemples.
- Garder `diagnosticsOnSave` active pour les debutants.

## Depannage extension

- Si le bouton Run ne fait rien : verifier `algolab.executablePath`.
- Si aucun diagnostic ne remonte : sauvegarder le fichier puis lancer "Vérifier AlgoLab".
- Si timeout frequent : augmenter `algolab.diagnosticsTimeoutMs`.
