# Configuration

Ce répertoire contient les fichiers de configuration pour le CryptoBot.

## Fichiers de configuration

### 🔑 API Keys
- `api_keys.env.example` - Modèle pour les clés API (à copier vers `api_keys.env`)
- `api_keys.env` - Fichiers des clés API réelles (non versionné)

### ⚙️ Configuration du bot
- `bot_config.json` - Configuration générale du bot
- `logging_config.json` - Configuration des logs
- `redis_config.json` - Configuration de la connexion Redis

### 📊 Paramètres d'analyse
- `technical_params.json` - Paramètres pour l'analyse technique
- `sentiment_params.json` - Paramètres pour l'analyse sentimentale
- `trading_params.json` - Paramètres pour les stratégies de trading

## Configuration des clés API

Pour configurer vos clés API:

1. Copiez le fichier exemple:
   ```bash
   cp config/api_keys.env.example config/api_keys.env
   ```

2. Éditez le fichier avec vos clés:
   ```bash
   nano config/api_keys.env
   ```

3. Sécurisez le fichier:
   ```bash
   chmod 600 config/api_keys.env
   ```

Le fichier `api_keys.env` doit contenir:

```
# Twitter API v2
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here

# HuggingFace
HUGGINGFACE_API_KEY=your_huggingface_key_here

# Anthropic (Claude AI)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Telegram (pour les notifications)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# CoinGecko
COINGECKO_API_KEY=your_coingecko_key_here
```

## Configuration du bot

Le fichier `bot_config.json` contient les paramètres généraux:

```json
{
  "general": {
    "environment": "production",
    "debug_mode": false,
    "notification_level": "important"
  },
  "data_collection": {
    "market_data_interval_minutes": 30,
    "sentiment_data_interval_minutes": 60,
    "youtube_check_interval_hours": 12
  },
  "analysis": {
    "technical_indicators": ["rsi", "sma", "macd", "bollinger"],
    "sentiment_sources": ["twitter", "reddit", "youtube"],
    "correlation_window_days": 7
  },
  "trading": {
    "portfolio_update_day": 1,
    "max_allocation_per_crypto": 0.4,
    "risk_tolerance": "medium"
  }
}
```

## Personnalisation

Vous pouvez personnaliser tous les paramètres selon vos besoins:

- Ajustez les intervalles de collecte de données
- Modifiez les indicateurs techniques utilisés
- Changez la stratégie de trading
- Configurez les niveaux de notification

## Sécurité

Les fichiers de configuration contenant des informations sensibles (comme `api_keys.env`) sont:
- Exclus du contrôle de version via `.gitignore`
- Protégés par des permissions restrictives
- Jamais exposés dans les logs ou l'interface

## Chargement de la configuration

Dans le code, la configuration est chargée comme suit:

```python
# Pour les clés API
import os
from dotenv import load_dotenv

load_dotenv('/path/to/config/api_keys.env')
twitter_api_key = os.getenv('TWITTER_API_KEY')

# Pour les fichiers JSON
import json

with open('/path/to/config/bot_config.json', 'r') as f:
    config = json.load(f)

debug_mode = config['general']['debug_mode']
```
