# FAQ et depannage (contenu de page documentation)

## Installation

### Q: `algolab` n'est pas reconnu, que faire ?

Verifier le PATH ou lancer le binaire avec son chemin complet.

### Q: Le binaire macOS ne s'execute pas.

Faire :

```bash
chmod +x ./algolab
```

Puis relancer.

### Q: Windows bloque l'executable telecharge.

Autoriser l'application depuis la fenetre de securite, puis retester.

## Execution des programmes

### Q: "Fichier introuvable"

Vous n'etes pas dans le bon dossier ou le nom de fichier est incorrect.

### Q: Le programme semble bloquer.

Verifier si votre code contient `LIRE` qui attend une entree utilisateur.

### Q: J'ai une erreur syntaxique.

Verifier en priorite :

- presence de `Debut` / `Fin`,
- fermetures des blocs (`FinSi`, `FinPour`, `FinTantQue`),
- expressions apres `Ecrire` et `LIRE`.

## Extension VS Code

### Q: Le bouton Run n'apparait pas.

Assurez-vous d'ouvrir un fichier avec extension `.algo`.

### Q: Les diagnostics n'apparaissent pas.

- Verifier `algolab.diagnosticsOnSave`.
- Lancer manuellement "Vérifier AlgoLab".
- Verifier `algolab.executablePath`.

### Q: J'ai un timeout de diagnostic.

Augmenter :

```json
"algolab.diagnosticsTimeoutMs": 5000
```

## Releases et versions

### Q: Quels fichiers dois-je telecharger ?

- Linux : `.deb`
- Windows : `algolab.exe`
- macOS : `algolab`
- VS Code : `algolab-vscode.vsix`

### Q: Comment savoir si ma version est a jour ?

Comparer votre release locale avec la derniere release GitHub.

## Support

Si le probleme persiste, ouvrir une issue avec :

1. OS et version,
2. version AlgoLab,
3. commande executee,
4. message d'erreur complet.
