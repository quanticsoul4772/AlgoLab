# Installation multi-OS (contenu de page documentation)

Ce guide est pret a etre publie comme page "Installation".

## Choisir votre mode d'installation

- **Linux** : paquet `.deb` (recommande).
- **Windows** : `algolab.exe`.
- **macOS** : binaire `algolab`.
- **Option Python** : `pip install .` pour developpeurs.

## Linux (Debian/Ubuntu)

### 1. Telecharger l'asset `.deb`

Depuis la derniere release GitHub.

### 2. Installer

```bash
sudo dpkg -i algolab_<version>_amd64.deb
```

### 3. Verifier

```bash
algolab --help
```

## macOS

### 1. Telecharger le binaire `algolab`

### 2. Rendre executable

```bash
chmod +x ./algolab
```

### 3. Tester

```bash
./algolab --help
```

### 4. (Optionnel) Installation globale

```bash
sudo mv ./algolab /usr/local/bin/algolab
algolab --help
```

## Windows

### 1. Telecharger `algolab.exe`

### 2. Ouvrir PowerShell dans le dossier de telechargement

### 3. Tester

```powershell
.\algolab.exe --help
```

### 4. (Optionnel) Ajouter au PATH

Ajoutez le dossier contenant `algolab.exe` a la variable d'environnement PATH.

## Option developpeur (Python)

Depuis la racine du projet :

```bash
pip install .
algolab --help
```

## Verification fonctionnelle finale

```bash
algolab -c "Variable x : Entier Debut x <- 7 Ecrire x Fin"
```

Sortie attendue : `7`

## Problemes courants

- **Commande introuvable** : PATH mal configure.
- **Permission refusee (macOS/Linux)** : faire `chmod +x`.
- **Blocage antivirus (Windows)** : autoriser le binaire telecharge.

## Lien utile

Pour l'utilisation apres installation, renvoyer vers :

- `GUIDE_UTILISATION.md`
