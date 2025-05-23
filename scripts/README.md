# Scripts

Ce répertoire contient les scripts utilitaires pour l'installation, la configuration et la maintenance du CryptoBot.

## Scripts disponibles

### 🚀 Installation et configuration

- `setup.sh` - Script principal d'installation et configuration
- `install_dependencies.sh` - Installation des dépendances système et Python
- `configure_redis.sh` - Configuration de Redis pour le stockage des données
- `setup_n8n.sh` - Installation et configuration de n8n

### 🔄 Exécution et maintenance

- `run.sh` - Démarrage de tous les composants (n8n, Flask, services)
- `backup_data.sh` - Sauvegarde des données importantes
- `cleanup_old_data.sh` - Nettoyage des anciennes données
- `update.sh` - Mise à jour du bot depuis le dépôt GitHub

### 🚢 Déploiement

- `deploy_ec2.sh` - Déploiement automatisé sur une instance EC2
- `setup_nginx.sh` - Configuration de Nginx comme proxy inverse
- `setup_ssl.sh` - Configuration des certificats SSL avec Let's Encrypt

## Utilisation

La plupart des scripts sont conçus pour être exécutés depuis la racine du projet:

```bash
# Installation complète
./scripts/setup.sh

# Démarrage du bot
./scripts/run.sh

# Sauvegarde des données
./scripts/backup_data.sh
```

## Personnalisation

Vous pouvez personnaliser les scripts en modifiant les variables en début de fichier. Par exemple, dans `setup.sh`:

```bash
# Variables de configuration
PYTHON_VERSION="3.8"
INSTALL_DIR="/home/crypto_bot"
USE_VIRTUAL_ENV=true
```

## Sécurité

Les scripts qui manipulent des informations sensibles (comme les clés API) sont conçus pour:
- Utiliser des variables d'environnement plutôt que des arguments en ligne de commande
- Définir des permissions restrictives sur les fichiers créés
- Ne jamais afficher d'informations sensibles dans les logs

## Développement

Pour contribuer aux scripts:

1. Assurez-vous qu'ils fonctionnent sur les plateformes cibles (Linux, macOS)
2. Ajoutez des commentaires explicatifs pour les sections complexes
3. Incluez des vérifications d'erreur et des messages utiles
4. Testez sur un environnement propre avant de soumettre

## Dépannage

Si vous rencontrez des problèmes avec les scripts:

1. Vérifiez les logs générés dans le dossier `logs/`
2. Exécutez les scripts avec l'option `-v` ou `--verbose` pour plus de détails
3. Consultez la section [Résolution des problèmes](../docs/troubleshooting.md) de la documentation
