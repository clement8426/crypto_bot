# Guide de Contribution

Merci de votre intérêt pour contribuer au projet CryptoBot ! Ce guide vous aidera à comprendre le processus de contribution.

## Table des matières

- [Code de conduite](#code-de-conduite)
- [Comment puis-je contribuer ?](#comment-puis-je-contribuer-)
  - [Signaler des bugs](#signaler-des-bugs)
  - [Suggérer des améliorations](#suggérer-des-améliorations)
  - [Contribuer au code](#contribuer-au-code)
- [Style de code](#style-de-code)
- [Processus de Pull Request](#processus-de-pull-request)
- [Environnement de développement](#environnement-de-développement)

## Code de conduite

Ce projet et tous ses participants sont régis par notre [Code de Conduite](CODE_OF_CONDUCT.md). En participant, vous êtes censé respecter ce code.

## Comment puis-je contribuer ?

### Signaler des bugs

Les bugs sont suivis comme des [issues GitHub](https://github.com/votre-username/crypto-bot/issues).

Lorsque vous créez une issue pour un bug, veuillez inclure :
- Un titre clair et descriptif
- Les étapes précises pour reproduire le problème
- Le comportement attendu et ce qui se passe réellement
- Des captures d'écran si possible
- Votre environnement (OS, version Python, etc.)

### Suggérer des améliorations

Les suggestions d'amélioration sont également suivies via les [issues GitHub](https://github.com/votre-username/crypto-bot/issues).

Pour suggérer une amélioration :
- Utilisez un titre clair et descriptif
- Décrivez en détail la fonctionnalité souhaitée
- Expliquez pourquoi cette fonctionnalité serait utile
- Proposez une implémentation si possible

### Contribuer au code

1. Forker le dépôt
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commiter vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## Style de code

Nous suivons les conventions de style suivantes :

- **Python** : [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **JavaScript** : [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **HTML/CSS** : [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)

Avant de soumettre votre code, assurez-vous qu'il respecte ces conventions. Vous pouvez utiliser des outils comme `flake8`, `eslint` et `stylelint`.

## Processus de Pull Request

1. Assurez-vous que votre code respecte nos conventions de style
2. Mettez à jour la documentation si nécessaire
3. Ajoutez des tests pour les nouvelles fonctionnalités
4. Assurez-vous que tous les tests passent
5. Soumettez votre Pull Request avec une description claire de ce qu'elle fait

Les Pull Requests sont examinées par au moins un membre de l'équipe. Nous pouvons demander des modifications avant de fusionner.

## Environnement de développement

Pour configurer votre environnement de développement :

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/crypto-bot.git
cd crypto-bot

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Configurer les hooks pre-commit
pre-commit install
```

## Structure des branches

- `main` : branche principale, toujours stable
- `develop` : branche de développement, intégration continue
- `feature/*` : branches pour les nouvelles fonctionnalités
- `bugfix/*` : branches pour les corrections de bugs
- `hotfix/*` : branches pour les corrections urgentes en production
- `release/*` : branches pour la préparation des releases

## Versionnement

Nous utilisons [SemVer](http://semver.org/) pour le versionnement. Les versions disponibles peuvent être consultées dans les [tags de ce dépôt](https://github.com/votre-username/crypto-bot/tags).

## Remerciements

Merci à tous ceux qui contribuent à ce projet !
