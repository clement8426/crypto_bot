# Source Code

Ce répertoire contient le code source Python du CryptoBot, organisé en modules fonctionnels.

## Structure

```
src/
├── analysis/           # Modules d'analyse (technique, sentimentale)
├── data_collection/    # Collecte de données (API, scraping)
├── trading/            # Logique de trading et recommandations
└── utils/              # Utilitaires communs
```

## Modules

### 📊 Analysis

Le module d'analyse contient les algorithmes pour:
- Analyse technique des prix et volumes
- Analyse sentimentale des réseaux sociaux
- Analyse de corrélation entre sentiment et prix
- Détection de patterns et signaux de trading

[En savoir plus sur le module Analysis](analysis/README.md)

### 📡 Data Collection

Le module de collecte de données gère:
- Connexion aux APIs de cryptomonnaies (CoinGecko, Binance, etc.)
- Scraping des réseaux sociaux (Twitter, Reddit)
- Transcription et analyse des vidéos YouTube
- Stockage et mise en cache des données

[En savoir plus sur le module Data Collection](data_collection/README.md)

### 💹 Trading

Le module de trading implémente:
- Stratégies d'investissement paramétrables
- Génération de recommandations d'achat/vente
- Allocation de portefeuille optimisée
- Backtesting et évaluation de performance

[En savoir plus sur le module Trading](trading/README.md)

### 🔧 Utils

Le module utils fournit:
- Fonctions d'aide communes
- Gestion des logs et erreurs
- Utilitaires de formatage et conversion
- Connecteurs Redis et base de données

[En savoir plus sur le module Utils](utils/README.md)

## Utilisation

Les modules sont conçus pour être utilisés ensemble ou indépendamment:

```python
# Exemple d'utilisation des modules
from src.data_collection.market_data import CoinGeckoCollector
from src.analysis.technical import TechnicalAnalyzer
from src.trading.portfolio import PortfolioOptimizer

# Collecter des données
collector = CoinGeckoCollector()
market_data = collector.get_market_data(['BTC', 'ETH', 'SOL'])

# Analyser les données
analyzer = TechnicalAnalyzer()
signals = analyzer.generate_signals(market_data)

# Générer des recommandations
optimizer = PortfolioOptimizer(initial_investment=50)
allocation = optimizer.optimize_portfolio(signals)
```

## Développement

Pour contribuer à ces modules:

1. Créez une branche pour votre fonctionnalité
2. Suivez les conventions de codage PEP 8
3. Ajoutez des tests unitaires dans le dossier `tests/`
4. Documentez votre code avec des docstrings
5. Soumettez une pull request
