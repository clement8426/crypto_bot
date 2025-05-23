# Interface Web Flask

Ce répertoire contient l'application web Flask qui sert d'interface utilisateur pour le CryptoBot.

## Structure

```
flask_app/
├── static/              # Ressources statiques
│   ├── css/             # Feuilles de style CSS
│   ├── js/              # Scripts JavaScript
│   └── img/             # Images et icônes
├── templates/           # Templates HTML Jinja2
├── app.py               # Point d'entrée de l'application
└── routes/              # Définitions des routes API et vues
```

## Fonctionnalités

L'interface web offre les fonctionnalités suivantes:

- **Dashboard principal**: Vue d'ensemble des performances et signaux
- **Analyse technique**: Graphiques interactifs avec indicateurs techniques
- **Analyse sentimentale**: Visualisation du sentiment des réseaux sociaux
- **Recommandations**: Suggestions d'allocation de portefeuille
- **Configuration**: Paramétrage du bot et des stratégies

## Technologies utilisées

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, Chart.js/Plotly.js
- **Temps réel**: Socket.IO pour les mises à jour en direct
- **Responsive**: Compatible mobile et desktop

## Installation

### Prérequis
- Python 3.8+
- Redis (pour le stockage des données en temps réel)

### Installation locale

```bash
# Depuis la racine du projet
cd flask_app

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application en mode développement
python app.py
```

L'application sera accessible à l'adresse: http://localhost:5000

### Déploiement en production

Pour un déploiement en production, nous recommandons:

```bash
# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Consultez le [guide de déploiement](../docs/deployment.md) pour une configuration avec Nginx et HTTPS.

## Personnalisation

### Thème et apparence

Vous pouvez personnaliser l'apparence en modifiant:
- `static/css/style.css` pour les styles personnalisés
- `templates/base.html` pour la structure globale

### Ajout de nouvelles pages

Pour ajouter une nouvelle page:

1. Créez un template dans `templates/`
2. Ajoutez une route dans `app.py` ou dans le module approprié dans `routes/`
3. Mettez à jour la navigation dans `templates/base.html`

## API REST

L'interface expose également une API REST pour l'intégration avec d'autres services:

- `GET /api/market-data`: Données de marché actuelles
- `GET /api/sentiment-data`: Données sentimentales récentes
- `GET /api/recommendations`: Dernières recommandations d'investissement

Consultez le [guide de l'API](../docs/api.md) pour la documentation complète.

## Développement

Pour contribuer au développement de l'interface:

1. Créez une branche pour votre fonctionnalité
2. Suivez les conventions de codage PEP 8 pour Python et les standards ESLint pour JavaScript
3. Testez sur différents navigateurs et tailles d'écran
4. Soumettez une pull request

## Captures d'écran

![Dashboard](../docs/images/dashboard_screenshot.png)
![Analyse Technique](../docs/images/technical_analysis_screenshot.png)
![Recommandations](../docs/images/recommendations_screenshot.png)
