#!/bin/bash
# Script d'installation et configuration du CryptoBot

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les étapes
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Vérifier les droits d'admin
if [ "$EUID" -ne 0 ]; then
    error "Ce script doit être exécuté avec les droits administrateur (sudo)"
fi

# Créer la structure de fichiers
log "Création de la structure de fichiers..."
mkdir -p /home/crypto_bot/{data,scripts,config,logs,backups}

# Définir les droits d'accès
chmod -R 755 /home/crypto_bot
chown -R $SUDO_USER:$SUDO_USER /home/crypto_bot

# Installer les dépendances système
log "Installation des dépendances système..."
apt update
apt install -y python3-pip python3-venv ffmpeg nodejs npm redis-server nginx

# Installer n8n
log "Installation de n8n..."
if ! command -v n8n &> /dev/null; then
    npm install n8n -g
else
    warning "n8n est déjà installé, mise à jour..."
    npm update n8n -g
fi

# Créer un environnement Python virtuel
log "Création d'un environnement Python virtuel..."
python3 -m venv /home/crypto_bot/venv
source /home/crypto_bot/venv/bin/activate

# Installer les dépendances Python
log "Installation des dépendances Python..."
pip install faster-whisper yt-dlp pandas numpy matplotlib flask gunicorn plotly redis python-dotenv

# Copier les fichiers depuis le dépôt
log "Copie des fichiers depuis le dépôt..."
cp -r src/* /home/crypto_bot/scripts/
cp -r workflows/* /home/crypto_bot/workflows/
cp -r flask_app/* /home/crypto_bot/flask_app/
cp -r config/* /home/crypto_bot/config/

# Rendre les scripts exécutables
chmod +x /home/crypto_bot/scripts/*.py
chmod +x /home/crypto_bot/scripts/*.sh

# Créer le fichier de configuration des clés API
log "Création du fichier de configuration des clés API..."
cat > /home/crypto_bot/config/api_keys.env << 'EOF'
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
EOF

# Sécuriser le fichier de configuration
chmod 600 /home/crypto_bot/config/api_keys.env

# Créer le service systemd pour n8n
log "Configuration du service n8n..."
cat > /etc/systemd/system/n8n.service << 'EOF'
[Unit]
Description=n8n Workflow Automation
After=network.target redis.service

[Service]
User=root
WorkingDirectory=/root/.n8n
Environment=NODE_ENV=production
Environment=N8N_BASIC_AUTH_ACTIVE=true
Environment=N8N_BASIC_AUTH_USER=admin
Environment=N8N_BASIC_AUTH_PASSWORD=changeme
ExecStart=/usr/bin/n8n start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Créer le service systemd pour Flask
log "Configuration du service Flask..."
cat > /etc/systemd/system/crypto-flask.service << 'EOF'
[Unit]
Description=Crypto Bot Flask Interface
After=network.target redis.service

[Service]
User=ubuntu
WorkingDirectory=/home/crypto_bot/flask_app
Environment="PATH=/home/crypto_bot/venv/bin"
ExecStart=/home/crypto_bot/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Recharger systemd et activer les services
systemctl daemon-reload
systemctl enable n8n
systemctl enable crypto-flask
systemctl enable redis
systemctl enable nginx

# Configurer Nginx
log "Configuration de Nginx..."
cat > /etc/nginx/sites-available/crypto-bot.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/crypto-bot.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Vérifier la configuration Nginx
nginx -t

# Initialiser les fichiers de données
log "Initialisation des fichiers de données..."
for file in emotional_data.json market_data.json video_analysis.json processed_videos.json fear_greed_index.json market_reports.json; do
    if [ ! -f "/home/crypto_bot/data/$file" ]; then
        echo "[]" > "/home/crypto_bot/data/$file"
    fi
done

# Démarrer les services
log "Démarrage des services..."
systemctl start redis
systemctl start n8n
systemctl start crypto-flask
systemctl restart nginx

log "Installation terminée!"
echo -e "\nPour finaliser l'installation:"
echo -e "1. Modifiez le fichier /home/crypto_bot/config/api_keys.env avec vos clés API"
echo -e "2. Accédez à n8n sur http://votre-ip:5678"
echo -e "3. Importez les workflows depuis le dossier /home/crypto_bot/workflows/"
echo -e "4. Accédez à l'interface web sur http://votre-ip"
echo -e "\nMerci d'utiliser CryptoBot!"
