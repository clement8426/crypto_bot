# Tests

Ce répertoire contient les tests unitaires et d'intégration pour le CryptoBot.

## Structure

```
tests/
├── unit/                # Tests unitaires
│   ├── analysis/        # Tests des modules d'analyse
│   ├── data_collection/ # Tests des modules de collecte de données
│   ├── trading/         # Tests des modules de trading
│   └── utils/           # Tests des utilitaires
├── integration/         # Tests d'intégration
│   ├── api/             # Tests de l'API REST
│   ├── workflows/       # Tests des workflows n8n
│   └── end_to_end/      # Tests de bout en bout
├── fixtures/            # Données de test
└── conftest.py          # Configuration pytest
```

## Exécution des tests

### Prérequis
- Python 3.8+
- pytest
- Environnement virtuel activé

### Exécuter tous les tests

```bash
# Depuis la racine du projet
pytest tests/
```

### Exécuter des tests spécifiques

```bash
# Tests unitaires uniquement
pytest tests/unit/

# Tests d'un module spécifique
pytest tests/unit/analysis/

# Tests d'intégration uniquement
pytest tests/integration/
```

### Exécuter avec couverture de code

```bash
pytest --cov=src tests/
```

## Écriture de nouveaux tests

### Tests unitaires

Les tests unitaires doivent:
- Tester une seule fonction ou méthode
- Être indépendants des autres tests
- Utiliser des mocks pour les dépendances externes
- Suivre la convention de nommage `test_*.py`

Exemple:

```python
# tests/unit/analysis/test_technical.py
import pytest
from src.analysis.technical import TechnicalAnalyzer

def test_rsi_calculation():
    analyzer = TechnicalAnalyzer()
    prices = [10, 11, 10.5, 10.8, 11.2, 11.5, 11.3]
    rsi = analyzer.calculate_rsi(prices)
    assert 30 <= rsi <= 70  # RSI devrait être dans une plage valide
```

### Tests d'intégration

Les tests d'intégration doivent:
- Tester l'interaction entre plusieurs composants
- Utiliser des fixtures pour les données partagées
- Minimiser les appels aux APIs externes
- Être organisés par fonctionnalité

Exemple:

```python
# tests/integration/api/test_market_data_api.py
import pytest
import requests
from flask_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_market_data_endpoint(client):
    response = client.get('/api/market-data')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'symbol' in data[0]
```

## Fixtures

Les fixtures sont des données ou des objets réutilisables pour les tests:

```python
# tests/fixtures/market_data.py
import pytest
import json
import os

@pytest.fixture
def sample_market_data():
    fixture_path = os.path.join(os.path.dirname(__file__), 'sample_market_data.json')
    with open(fixture_path, 'r') as f:
        return json.load(f)
```

## Mocks

Utilisez des mocks pour simuler les dépendances externes:

```python
# tests/unit/data_collection/test_market_data.py
import pytest
from unittest.mock import patch, MagicMock
from src.data_collection.market_data import CoinGeckoCollector

def test_get_market_data():
    # Simuler la réponse de l'API CoinGecko
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": "bitcoin", "symbol": "btc", "current_price": 50000}
    ]
    
    with patch('requests.get', return_value=mock_response):
        collector = CoinGeckoCollector()
        data = collector.get_market_data(['btc'])
        
        assert len(data) == 1
        assert data[0]['symbol'] == 'BTC'
        assert data[0]['price'] == 50000
```

## Bonnes pratiques

- Exécutez les tests avant chaque commit
- Maintenez une couverture de code élevée (>80%)
- Utilisez des assertions claires et spécifiques
- Documentez le but de chaque test
- Organisez les tests par module et fonctionnalité
- Utilisez des fixtures pour éviter la duplication de code

## Intégration continue

Les tests sont automatiquement exécutés dans le pipeline CI:

- À chaque push sur une branche
- À chaque pull request
- Avant chaque déploiement

Consultez le [workflow GitHub Actions](../.github/workflows/tests.yml) pour plus de détails.
