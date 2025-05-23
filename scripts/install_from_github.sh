#!/bin/bash
# Script d'installation rapide pour CryptoBot depuis GitHub

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

# Vérifier si le script est exécuté avec sudo
if [ "$EUID" -ne 0 ]; then
    error "Ce script doit être exécuté avec les droits administrateur (sudo)"
fi

# Demander le répertoire d'installation
read -p "Répertoire d'installation [/home/crypto_bot]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-/home/crypto_bot}

# Créer le répertoire d'installation
log "Création du répertoire d'installation: $INSTALL_DIR"
mkdir -p $INSTALL_DIR
if [ $? -ne 0 ]; then
    error "Impossible de créer le répertoire d'installation"
fi

# Installer les dépendances système
log "Installation des dépendances système..."
apt update
apt install -y python3-pip python3-venv ffmpeg nodejs npm redis-server nginx curl git

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
python3 -m venv $INSTALL_DIR/venv
source $INSTALL_DIR/venv/bin/activate

# Installer les dépendances Python
log "Installation des dépendances Python..."
pip install faster-whisper yt-dlp pandas numpy matplotlib flask gunicorn plotly redis python-dotenv requests beautifulsoup4

# Cloner le dépôt GitHub
log "Clonage du dépôt GitHub..."
TEMP_DIR=$(mktemp -d)
git clone https://github.com/votre-username/crypto-bot.git $TEMP_DIR
if [ $? -ne 0 ]; then
    error "Impossible de cloner le dépôt GitHub"
fi

# Créer la structure de répertoires
log "Création de la structure de répertoires..."
mkdir -p $INSTALL_DIR/{data,logs,scripts,config,workflows,flask_app,backups}
mkdir -p $INSTALL_DIR/data/{transcripts}

# Copier les fichiers depuis le dépôt cloné
log "Copie des fichiers depuis le dépôt..."
cp -r $TEMP_DIR/src/* $INSTALL_DIR/scripts/
cp -r $TEMP_DIR/workflows/* $INSTALL_DIR/workflows/
cp -r $TEMP_DIR/flask_app/* $INSTALL_DIR/flask_app/
cp -r $TEMP_DIR/config/* $INSTALL_DIR/config/
cp $TEMP_DIR/scripts/setup.sh $INSTALL_DIR/

# Nettoyer le répertoire temporaire
rm -rf $TEMP_DIR

# Rendre les scripts exécutables
chmod +x $INSTALL_DIR/scripts/*.py
chmod +x $INSTALL_DIR/scripts/*.sh
chmod +x $INSTALL_DIR/setup.sh

# Configurer les fichiers d'environnement
log "Configuration des fichiers d'environnement..."
if [ ! -f "$INSTALL_DIR/config/api_keys.env" ]; then
    cp $INSTALL_DIR/config/api_keys.env.example $INSTALL_DIR/config/api_keys.env
    chmod 600 $INSTALL_DIR/config/api_keys.env
    warning "Vous devez éditer le fichier $INSTALL_DIR/config/api_keys.env avec vos propres clés API"
fi

# Créer le service systemd pour n8n
log "Configuration du service n8n..."
cat > /etc/systemd/system/n8n.service << EOF
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
cat > /etc/systemd/system/crypto-flask.service << EOF
[Unit]
Description=Crypto Bot Flask Interface
After=network.target redis.service

[Service]
User=$(logname)
WorkingDirectory=$INSTALL_DIR/flask_app
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
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
cat > /etc/nginx/sites-available/crypto-bot.conf << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
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
    if [ ! -f "$INSTALL_DIR/data/$file" ]; then
        echo "[]" > "$INSTALL_DIR/data/$file"
    fi
done

# Définir les permissions
log "Configuration des permissions..."
chown -R $(logname):$(logname) $INSTALL_DIR
chmod -R 755 $INSTALL_DIR
chmod 600 $INSTALL_DIR/config/api_keys.env

# Démarrer les services
log "Démarrage des services..."
systemctl start redis
systemctl start n8n
systemctl start crypto-flask
systemctl restart nginx

log "Installation terminée avec succès!"
echo -e "\nPour finaliser l'installation:"
echo -e "1. Modifiez le fichier $INSTALL_DIR/config/api_keys.env avec vos clés API"
echo -e "2. Accédez à n8n sur http://votre-ip:5678"
echo -e "3. Importez les workflows depuis le dossier $INSTALL_DIR/workflows/"
echo -e "4. Accédez à l'interface web sur http://votre-ip"
echo -e "\nMerci d'utiliser CryptoBot!"
