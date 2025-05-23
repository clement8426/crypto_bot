from flask import Flask, render_template, jsonify, request
import redis
import json
import os
from dotenv import load_dotenv
import pandas as pd
import plotly
import plotly.express as px
from datetime import datetime, timedelta
import threading
import time
import logging
from typing import Dict, List

# Charger les variables d'environnement
load_dotenv('/home/crypto_bot/config/api_keys.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crypto_bot_secret_key_2024'

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class DashboardManager:
    """Gestionnaire du dashboard en temps réel"""
    
    def __init__(self):
        self.active_connections = 0
        self.last_update = datetime.now()
        self.logger = logging.getLogger('dashboard_manager')
        
    def get_trading_summary(self) -> Dict:
        """Récupère le résumé de trading"""
        try:
            # Rapport quotidien
            report_data = redis_client.get("daily_report")
            report = json.loads(report_data) if report_data else {}
            
            # Résumé du scan
            scan_data = redis_client.get("scan_summary")
            scan = json.loads(scan_data) if scan_data else {}
            
            # Positions ouvertes
            positions_data = redis_client.get("open_positions")
            positions = json.loads(positions_data) if positions_data else []
            
            # Signaux récents
            signals_data = redis_client.get("recent_signals")
            signals = json.loads(signals_data) if signals_data else []
            
            return {
                "report": report,
                "scan": scan,
                "positions": positions,
                "signals": signals,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération du résumé de trading: {str(e)}")
            return {"error": str(e)}
    
    def get_market_data(self, symbols: List[str] = None) -> Dict:
        """Récupère les données de marché pour les symboles spécifiés"""
        try:
            # Si aucun symbole n'est spécifié, utiliser les symboles par défaut
            if not symbols:
                symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'BNB', 'DOT', 'XRP']
            
            result = {}
            
            for symbol in symbols:
                # Récupérer les données de marché depuis Redis
                market_data = redis_client.get(f"market_data:{symbol}")
                
                if market_data:
                    result[symbol] = json.loads(market_data)
                else:
                    # Charger depuis le fichier JSON si non disponible dans Redis
                    try:
                        with open(f'/home/crypto_bot/data/market_data.json', 'r') as f:
                            all_data = json.load(f)
                            symbol_data = [item for item in all_data if item['symbol'] == symbol]
                            if symbol_data:
                                # Trier par timestamp décroissant
                                symbol_data.sort(key=lambda x: x['timestamp'], reverse=True)
                                result[symbol] = symbol_data[0]  # Prendre la donnée la plus récente
                    except Exception as e:
                        self.logger.error(f"Erreur lors de la lecture du fichier market_data.json: {str(e)}")
            
            return {
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des données de marché: {str(e)}")
            return {"error": str(e)}
    
    def get_sentiment_data(self, hours_back: int = 24) -> Dict:
        """Récupère les données sentimentales des dernières heures"""
        try:
            # Calculer la date limite
            cutoff_date = datetime.now() - timedelta(hours=hours_back)
            cutoff_str = cutoff_date.isoformat()
            
            # Récupérer les données sentimentales depuis Redis
            sentiment_data = redis_client.get("sentiment_data")
            
            if sentiment_data:
                data = json.loads(sentiment_data)
            else:
                # Charger depuis le fichier JSON si non disponible dans Redis
                try:
                    with open('/home/crypto_bot/data/emotional_data.json', 'r') as f:
                        data = json.load(f)
                except Exception as e:
                    self.logger.error(f"Erreur lors de la lecture du fichier emotional_data.json: {str(e)}")
                    data = []
            
            # Filtrer les données par date
            recent_data = [item for item in data if item.get('timestamp', '') > cutoff_str]
            
            # Agréger les sentiments
            sentiment_counts = {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            }
            
            for item in recent_data:
                sentiment = item.get('sentiment', 'neutral')
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1
            
            # Calculer les pourcentages
            total = sum(sentiment_counts.values()) or 1  # Éviter division par zéro
            sentiment_percentages = {
                k: round(v / total * 100, 1) for k, v in sentiment_counts.items()
            }
            
            return {
                "counts": sentiment_counts,
                "percentages": sentiment_percentages,
                "total_items": len(recent_data),
                "hours_analyzed": hours_back,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des données sentimentales: {str(e)}")
            return {"error": str(e)}
    
    def get_technical_indicators(self, symbol: str) -> Dict:
        """Récupère les indicateurs techniques pour un symbole spécifique"""
        try:
            # Récupérer les indicateurs techniques depuis Redis
            indicators_data = redis_client.get(f"technical_indicators:{symbol}")
            
            if indicators_data:
                return json.loads(indicators_data)
            else:
                # Charger depuis le fichier JSON si non disponible dans Redis
                try:
                    with open('/home/crypto_bot/data/market_data.json', 'r') as f:
                        all_data = json.load(f)
                        symbol_data = [item for item in all_data if item['symbol'] == symbol]
                        
                        if symbol_data:
                            # Trier par timestamp décroissant
                            symbol_data.sort(key=lambda x: x['timestamp'], reverse=True)
                            latest_data = symbol_data[0]
                            
                            # Extraire les indicateurs techniques
                            return {
                                "symbol": symbol,
                                "indicators": latest_data.get('technical_indicators', {}),
                                "signal": latest_data.get('technical_signal', 'NEUTRAL'),
                                "timestamp": latest_data.get('timestamp', datetime.now().isoformat())
                            }
                except Exception as e:
                    self.logger.error(f"Erreur lors de la lecture du fichier market_data.json: {str(e)}")
            
            return {
                "symbol": symbol,
                "indicators": {},
                "signal": "NEUTRAL",
                "timestamp": datetime.now().isoformat(),
                "error": "Données non disponibles"
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des indicateurs techniques: {str(e)}")
            return {"error": str(e)}
    
    def get_portfolio_recommendations(self) -> Dict:
        """Récupère les recommandations pour le portefeuille"""
        try:
            # Récupérer les recommandations depuis Redis
            recommendations_data = redis_client.get("portfolio_recommendations")
            
            if recommendations_data:
                return json.loads(recommendations_data)
            else:
                # Charger depuis le fichier JSON si non disponible dans Redis
                try:
                    with open('/home/crypto_bot/data/market_reports.json', 'r') as f:
                        reports = json.load(f)
                        if reports:
                            latest_report = reports[0]
                            
                            # Extraire les recommandations
                            return {
                                "report_date": latest_report.get('date', ''),
                                "market_summary": latest_report.get('market_summary', {}),
                                "recommendations": latest_report.get('crypto_data', {}),
                                "market_trends": latest_report.get('market_trends', {}),
                                "timestamp": datetime.now().isoformat()
                            }
                except Exception as e:
                    self.logger.error(f"Erreur lors de la lecture du fichier market_reports.json: {str(e)}")
            
            return {
                "report_date": "",
                "market_summary": {},
                "recommendations": {},
                "market_trends": {},
                "timestamp": datetime.now().isoformat(),
                "error": "Données non disponibles"
            }
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des recommandations: {str(e)}")
            return {"error": str(e)}

# Initialiser le gestionnaire de dashboard
dashboard_manager = DashboardManager()

@app.route('/')
def index():
    """Page d'accueil du dashboard"""
    return render_template('index.html')

@app.route('/detail/<symbol>')
def detail(symbol):
    """Page de détail pour un symbole spécifique"""
    return render_template('detail/index.html', symbol=symbol)

@app.route('/market')
def market():
    """Page d'aperçu du marché"""
    return render_template('market/index.html')

@app.route('/signals')
def signals():
    """Page des signaux de trading"""
    return render_template('signals/index.html')

@app.route('/settings')
def settings():
    """Page des paramètres"""
    return render_template('settings/index.html')

@app.route('/api/trading-summary')
def api_trading_summary():
    """API pour récupérer le résumé de trading"""
    return jsonify(dashboard_manager.get_trading_summary())

@app.route('/api/market-data')
def api_market_data():
    """API pour récupérer les données de marché"""
    symbols = request.args.get('symbols')
    if symbols:
        symbols = symbols.split(',')
    return jsonify(dashboard_manager.get_market_data(symbols))

@app.route('/api/sentiment-data')
def api_sentiment_data():
    """API pour récupérer les données sentimentales"""
    hours_back = request.args.get('hours', 24, type=int)
    return jsonify(dashboard_manager.get_sentiment_data(hours_back))

@app.route('/api/technical-indicators/<symbol>')
def api_technical_indicators(symbol):
    """API pour récupérer les indicateurs techniques"""
    return jsonify(dashboard_manager.get_technical_indicators(symbol))

@app.route('/api/portfolio-recommendations')
def api_portfolio_recommendations():
    """API pour récupérer les recommandations de portefeuille"""
    return jsonify(dashboard_manager.get_portfolio_recommendations())

# Fonction pour mettre à jour périodiquement les données dans Redis
def update_redis_cache():
    """Met à jour périodiquement les données dans Redis"""
    while True:
        try:
            # Charger les données de marché
            try:
                with open('/home/crypto_bot/data/market_data.json', 'r') as f:
                    market_data = json.load(f)
                    
                    # Organiser par symbole
                    symbols = set(item['symbol'] for item in market_data)
                    
                    for symbol in symbols:
                        symbol_data = [item for item in market_data if item['symbol'] == symbol]
                        symbol_data.sort(key=lambda x: x['timestamp'], reverse=True)
                        
                        if symbol_data:
                            # Stocker dans Redis avec expiration de 1 heure
                            redis_client.setex(
                                f"market_data:{symbol}", 
                                3600, 
                                json.dumps(symbol_data[0])
                            )
            except Exception as e:
                logging.error(f"Erreur lors de la mise à jour des données de marché: {str(e)}")
            
            # Charger les données sentimentales
            try:
                with open('/home/crypto_bot/data/emotional_data.json', 'r') as f:
                    sentiment_data = json.load(f)
                    
                    # Prendre les 1000 dernières entrées maximum
                    recent_data = sentiment_data[-1000:]
                    
                    # Stocker dans Redis avec expiration de 1 heure
                    redis_client.setex(
                        "sentiment_data", 
                        3600, 
                        json.dumps(recent_data)
                    )
            except Exception as e:
                logging.error(f"Erreur lors de la mise à jour des données sentimentales: {str(e)}")
            
            # Charger les rapports de marché
            try:
                with open('/home/crypto_bot/data/market_reports.json', 'r') as f:
                    reports = json.load(f)
                    
                    if reports:
                        # Stocker dans Redis avec expiration de 1 jour
                        redis_client.setex(
                            "portfolio_recommendations", 
                            86400, 
                            json.dumps(reports[0])
                        )
            except Exception as e:
                logging.error(f"Erreur lors de la mise à jour des recommandations: {str(e)}")
                
        except Exception as e:
            logging.error(f"Erreur dans la tâche de mise à jour Redis: {str(e)}")
        
        # Attendre 5 minutes avant la prochaine mise à jour
        time.sleep(300)

if __name__ == '__main__':
    # Configurer le logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/home/crypto_bot/logs/flask_app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Démarrer la tâche de mise à jour Redis dans un thread séparé
    update_thread = threading.Thread(target=update_redis_cache, daemon=True)
    update_thread.start()
    
    # Démarrer l'application Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
