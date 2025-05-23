# Workflows n8n

Ce répertoire contient les workflows n8n pour l'automatisation des tâches d'analyse et de trading crypto.

## Présentation

[n8n](https://n8n.io/) est une plateforme d'automatisation de flux de travail qui nous permet d'orchestrer les différentes composantes du CryptoBot sans code. Les workflows sont exportés au format JSON et peuvent être importés dans n'importe quelle instance n8n.

## Workflows disponibles

### 📊 Analyse de Marché
`workflow_n8n_analyse_marche.json`

Ce workflow collecte et analyse les données techniques du marché crypto:
- Collecte des prix et volumes via CoinGecko
- Calcul des indicateurs techniques (RSI, SMA, etc.)
- Détection des signaux d'achat/vente
- Génération de rapports quotidiens

**Fréquence d'exécution**: Toutes les 30 minutes

### 💬 Analyse Sentimentale
`workflow_n8n_analyse_sentiment.json`

Ce workflow surveille et analyse le sentiment sur les réseaux sociaux:
- Collecte des tweets et posts Reddit sur les cryptomonnaies
- Analyse du sentiment via HuggingFace
- Détection des tendances et émotions dominantes
- Stockage des données sentimentales

**Fréquence d'exécution**: Toutes les heures

### 📹 Analyse YouTube
`workflow_n8n_analyse_youtube.json`

Ce workflow transcrit et analyse les vidéos YouTube pertinentes:
- Surveillance des chaînes YouTube crypto
- Téléchargement et transcription des nouvelles vidéos
- Analyse du contenu transcrit
- Extraction des informations clés

**Fréquence d'exécution**: Deux fois par jour

## Installation

Pour importer ces workflows dans votre instance n8n:

1. Accédez à votre interface n8n (par défaut: http://localhost:5678)
2. Cliquez sur "Workflows" dans le menu de gauche
3. Cliquez sur le bouton "Import from File"
4. Sélectionnez le fichier JSON du workflow à importer
5. Configurez les credentials nécessaires (API keys)
6. Activez le workflow

## Configuration des Credentials

Les workflows nécessitent les credentials suivants:

- **Twitter**: Clés API Twitter v2
- **Reddit**: Identifiants OAuth Reddit
- **HuggingFace**: Clé API pour l'analyse de sentiment
- **Anthropic**: Clé API pour l'analyse de contenu
- **CoinGecko**: Clé API Pro (optionnelle)

Consultez le [guide de configuration](../docs/configuration.md) pour plus de détails.

## Personnalisation

Vous pouvez personnaliser les workflows selon vos besoins:

- Modifier les cryptomonnaies surveillées
- Ajuster les fréquences d'exécution
- Ajouter de nouvelles sources de données
- Personnaliser les seuils des indicateurs techniques

## Dépannage

Si vous rencontrez des problèmes avec les workflows:

1. Vérifiez les logs d'exécution dans n8n
2. Assurez-vous que toutes les credentials sont correctement configurées
3. Vérifiez que les APIs externes sont accessibles
4. Consultez la [documentation n8n](https://docs.n8n.io/) pour plus d'aide

## Ressources

- [Documentation officielle n8n](https://docs.n8n.io/)
- [Communauté n8n](https://community.n8n.io/)
- [Tutoriels vidéo n8n](https://www.youtube.com/c/n8nio)
