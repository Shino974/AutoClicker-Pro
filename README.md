# Auto Clicker Pro - Anti-Detection 🎯

Un auto-clicker avancé avec système anti-détection pour contourner les protections des jeux et applications. Interface moderne et responsive avec de nombreuses fonctionnalités.

## ✨ Fonctionnalités

### 🛡️ Anti-Détection Avancée
- **3 méthodes de clic** : Windows API, SendMessage, PostMessage
- **Humanisation des clics** : Variations de position (±2 pixels)
- **Timing variable** : Intervalles aléatoires pour imiter le comportement humain
- **Micro-pauses** : Délais variables entre press/release (10-50ms)

### ⚡ Configuration Flexible
- **Sélection de position** : Overlay plein écran avec curseur croix
- **Presets de fréquence** : Lent, Normal, Rapide, Ultra
- **Intervalle personnalisé** : De 0.01 à 10 secondes
- **Nombre de clics** : Infini ou nombre personnalisé

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- Windows (pour les fonctionnalités anti-détection)

### Installation rapide
```bash
# Cloner le repository
git clone https://github.com/votre-username/auto-clicker-pro.git
cd auto-clicker-pro

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Dépendances
```
keyboard==0.13.5   # Raccourcis globaux
pywin32==311       # API Windows pour anti-détection
```

## 📖 Guide d'utilisation

### 1. Configuration de base
1. **Sélectionner une position** : Cliquez sur "🎯 Sélectionner Position"
2. **Choisir la fréquence** : Utilisez les presets ou définissez un intervalle
3. **Configurer le nombre** : Infini ou nombre personnalisé

### 2. Options anti-détection
- **Windows API** (Recommandé) : Méthode la plus naturelle
- **SendMessage** : Messages directs à la fenêtre
- **PostMessage** : Messages asynchrones
- **Humanisation** : Active les variations naturelles
- **Intervalles aléatoires** : ±50% de variation

### 3. Contrôles
- **F6** ou bouton vert : Démarrer l'auto-clicker
- **F7** ou bouton rouge : Arrêter l'auto-clicker
- **Molette** : Scroll dans l'interface
- **▼/▶** : Réduire/étendre les sections

## 🎮 Compatibilité jeux

### ✅ Testé et fonctionnel
- Cookie Clicker
- Clicker Heroes
- Adventure Capitalist
- Idle Champions
- La plupart des jeux clicker web

### 🛡️ Méthodes recommandées par type
- **Jeux web** : Windows API + Humanisation
- **Applications desktop** : SendMessage
- **Jeux protégés** : PostMessage + Intervalles aléatoires

## ⚙️ Configuration avancée

### Paramètres anti-détection optimaux
```
Méthode: Windows API
Humanisation: ✅ Activée
Intervalles aléatoires: ✅ Activés
Fréquence: 0.5-1 seconde (pour éviter la détection)
```

### Personnalisation
Vous pouvez modifier les paramètres dans le code :
- `AdvancedClicker.human_like_click()` : Ajuster les variations
- `random.uniform(0.5, 1.5)` : Modifier la plage d'intervalles
- Couleurs de l'interface dans `setup_ui()`

## 🔧 Développement

### Structure du projet
```
auto-clicker-pro/
├── main.py              # Application principale
├── requirements.txt     # Dépendances Python
├── README.md           # Documentation
├── .gitignore          # Fichiers ignorés par Git
└── assets/             # (Future) Images et ressources
```

### Classes principales
- `AutoClickerApp` : Interface utilisateur
- `AdvancedClicker` : Logique de clic anti-détection

### Contribution
1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 🐛 Problèmes connus

### Windows Defender
Parfois détecté comme "potentiellement indésirable" :
```bash
# Ajouter une exception dans Windows Defender
# Paramètres > Mise à jour et sécurité > Sécurité Windows > Protection contre les virus
```

### Permissions administrateur
Certains jeux nécessitent des privilèges élevés :
```bash
# Lancer en tant qu'administrateur
python main.py
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Cet outil est destiné à des fins éducatives et de test. L'utilisation dans des jeux en ligne peut violer les conditions d'utilisation. Utilisez à vos propres risques.

## 👤 Auteur

**Shino974**
- Email: theotrp.pro@gmail.com
- GitHub: [@Shino974](https://github.com/Shino974)

## 🙏 Remerciements

- [keyboard](https://github.com/boppreh/keyboard) pour les raccourcis globaux
- [pywin32](https://github.com/mhammond/pywin32) pour les API Windows

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous a aidé !** ⭐
