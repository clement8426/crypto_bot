# CryptoBot - Plateforme d'Analyse et Trading Crypto

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Vue d'ensemble

CryptoBot est une plateforme complète d'analyse et de trading de cryptomonnaies qui combine analyse sentimentale, analyse technique et machine learning pour générer des recommandations d'investissement optimisées.

![Architecture](docs/images/architecture_overview.png)

### 🌟 Caractéristiques principales

- **Analyse multi-sources** : Données de marché, réseaux sociaux et contenu YouTube
- **Workflows automatisés** : Orchestration via n8n pour une analyse continue
- **Interface web intuitive** : Dashboard Flask avec visualisations Plotly
- **Stratégie d'investissement** : Recommandations mensuelles pour un portefeuille diversifié
- **Déploiement simplifié** : Configuration automatisée pour EC2

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- Node.js 14+
- Redis
- Compte AWS (pour déploiement EC2)

### Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/crypto-bot.git
cd crypto-bot

# Installer les dépendances
./scripts/setup.sh

# Configurer les clés API
cp config/api_keys.env.example config/api_keys.env
# Éditer config/api_keys.env avec vos clés API

# Lancer l'application
./scripts/run.sh
```

### Déploiement sur EC2

```bash
# Configurer une instance EC2
./scripts/deploy_ec2.sh
```

Pour des instructions détaillées, consultez notre [Guide de déploiement](docs/deployment.md).

## 📂 Structure du projet

```
crypto-bot/
├── src/                    # Code source Python
│   ├── analysis/           # Modules d'analyse (technique, sentimentale)
│   ├── data_collection/    # Collecte de données (API, scraping)
│   ├── trading/            # Logique de trading et recommandations
│   └── utils/              # Utilitaires communs
├── workflows/              # Workflows n8n
├── flask_app/              # Interface web Flask
├── docs/                   # Documentation
├── scripts/                # Scripts d'installation et utilitaires
├── config/                 # Fichiers de configuration
└── tests/                  # Tests unitaires et d'intégration
```

Chaque dossier contient son propre README avec des informations spécifiques.

## 📚 Documentation

- [Guide d'architecture](docs/architecture.md)
- [Guide d'installation](docs/installation.md)
- [Guide de l'API](docs/api.md)
- [Guide de l'interface web](docs/web_interface.md)
- [Guide des workflows](docs/workflows.md)
- [Guide de contribution](CONTRIBUTING.md)

## 🔧 Configuration

La configuration se fait principalement via les fichiers dans le dossier `config/`:

- `api_keys.env` - Clés API pour les services externes
- `bot_config.json` - Configuration des paramètres du bot
- `trading_params.json` - Paramètres de la stratégie de trading

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre [Guide de contribution](CONTRIBUTING.md) pour commencer.

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📞 Support

Pour toute question ou assistance, veuillez [ouvrir une issue](https://github.com/votre-username/crypto-bot/issues) ou contacter l'équipe de développement.
# vps-crypto-bot-n8n-flask
