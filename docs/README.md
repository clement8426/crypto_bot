# Documentation

Ce répertoire contient la documentation complète du CryptoBot, organisée par thématiques.

## Guides disponibles

### 📐 Architecture
- [Vue d'ensemble de l'architecture](architecture.md)
- [Flux de données](data_flow.md)
- [Intégration des composants](component_integration.md)

### 🚀 Installation et déploiement
- [Installation locale](installation.md)
- [Déploiement sur EC2](deployment.md)
- [Configuration des services](services_configuration.md)

### 💻 Développement
- [Guide du développeur](developer_guide.md)
- [Conventions de codage](coding_conventions.md)
- [Tests et qualité du code](testing.md)

### 🔌 API et intégrations
- [Documentation de l'API REST](api.md)
- [Webhooks](webhooks.md)
- [Intégration avec d'autres services](integrations.md)

### 📊 Utilisation
- [Guide de l'interface web](web_interface.md)
- [Interprétation des signaux](signals_guide.md)
- [Stratégies d'investissement](investment_strategies.md)

## Images et diagrammes

Le sous-répertoire `images/` contient tous les diagrammes et captures d'écran utilisés dans la documentation:

```
images/
├── architecture_overview.png    # Vue d'ensemble de l'architecture
├── data_flow_diagram.png        # Diagramme de flux de données
├── dashboard_screenshot.png     # Capture d'écran du dashboard
├── technical_analysis_screenshot.png  # Capture d'écran de l'analyse technique
└── recommendations_screenshot.png     # Capture d'écran des recommandations
```

## Contribution à la documentation

La documentation est écrite en Markdown pour faciliter les contributions. Pour contribuer:

1. Créez une branche pour vos modifications
2. Suivez les conventions de formatage Markdown
3. Utilisez des liens relatifs pour référencer d'autres documents
4. Ajoutez des images dans le dossier `images/` si nécessaire
5. Soumettez une pull request

## Génération de documentation

Pour générer une version HTML de la documentation:

```bash
# Depuis la racine du projet
cd docs
pip install mkdocs
mkdocs build
```

La documentation HTML sera générée dans le dossier `site/`.

## Ressources externes

- [Guide officiel de Markdown](https://www.markdownguide.org/)
- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation n8n](https://docs.n8n.io/)
- [Documentation CoinGecko API](https://www.coingecko.com/api/documentation)
