import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/crypto_bot/logs/correlation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('correlation_analysis')

def load_data():
    """
    Charge les données de marché et sentimentales depuis les fichiers JSON
    
    Returns:
        tuple: (données de marché, données sentimentales)
    """
    try:
        # Charger les données de marché
        with open('/home/crypto_bot/data/market_data.json', 'r') as f:
            market_data = json.load(f)
        
        # Charger les données sentimentales
        with open('/home/crypto_bot/data/emotional_data.json', 'r') as f:
            sentiment_data = json.load(f)
        
        logger.info(f"Données chargées: {len(market_data)} entrées de marché, {len(sentiment_data)} entrées sentimentales")
        return market_data, sentiment_data
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données: {str(e)}")
        return [], []

def preprocess_market_data(market_data):
    """
    Prétraite les données de marché
    
    Args:
        market_data (list): Liste des données de marché
        
    Returns:
        dict: Données de marché prétraitées par symbole
    """
    try:
        # Convertir en DataFrame
        df = pd.DataFrame(market_data)
        
        # Convertir les timestamps en datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Trier par timestamp
        df = df.sort_values('timestamp')
        
        # Organiser par symbole
        result = {}
        for symbol in df['symbol'].unique():
            symbol_df = df[df['symbol'] == symbol].copy()
            
            # Ajouter des colonnes pour les variations de prix
            symbol_df['price_change'] = symbol_df['price'].pct_change()
            symbol_df['price_change_1h'] = symbol_df['price'].pct_change(periods=2)  # Approximation pour 1h
            symbol_df['price_change_24h'] = symbol_df['price'].pct_change(periods=48)  # Approximation pour 24h
            
            result[symbol] = symbol_df
        
        return result
    except Exception as e:
        logger.error(f"Erreur lors du prétraitement des données de marché: {str(e)}")
        return {}

def preprocess_sentiment_data(sentiment_data):
    """
    Prétraite les données sentimentales
    
    Args:
        sentiment_data (list): Liste des données sentimentales
        
    Returns:
        dict: Données sentimentales prétraitées par symbole
    """
    try:
        # Convertir en DataFrame
        df = pd.DataFrame(sentiment_data)
        
        # Convertir les timestamps en datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Trier par timestamp
        df = df.sort_values('timestamp')
        
        # Convertir le sentiment en valeur numérique
        sentiment_map = {
            'positive': 1,
            'neutral': 0,
            'negative': -1
        }
        df['sentiment_value'] = df['sentiment'].map(sentiment_map)
        
        # Organiser par symbole (related_crypto)
        result = {}
        symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'BNB', 'DOT', 'XRP']
        
        for symbol in symbols:
            # Filtrer les entrées liées à ce symbole
            symbol_df = df[df['related_crypto'].apply(lambda x: symbol in x if isinstance(x, list) else False)].copy()
            
            # Agréger par heure
            symbol_df['hour'] = symbol_df['timestamp'].dt.floor('H')
            hourly_sentiment = symbol_df.groupby('hour')['sentiment_value'].mean().reset_index()
            hourly_sentiment.columns = ['timestamp', 'sentiment_value']
            
            result[symbol] = hourly_sentiment
        
        return result
    except Exception as e:
        logger.error(f"Erreur lors du prétraitement des données sentimentales: {str(e)}")
        return {}

def calculate_correlation(market_data_by_symbol, sentiment_data_by_symbol, window_days=7):
    """
    Calcule la corrélation entre les données de marché et sentimentales
    
    Args:
        market_data_by_symbol (dict): Données de marché par symbole
        sentiment_data_by_symbol (dict): Données sentimentales par symbole
        window_days (int): Fenêtre de corrélation en jours
        
    Returns:
        dict: Résultats de corrélation par symbole
    """
    try:
        results = {}
        
        for symbol in market_data_by_symbol.keys():
            if symbol not in sentiment_data_by_symbol:
                continue
            
            market_df = market_data_by_symbol[symbol]
            sentiment_df = sentiment_data_by_symbol[symbol]
            
            # Fusionner les données sur le timestamp
            merged_df = pd.merge_asof(
                market_df, 
                sentiment_df, 
                on='timestamp',
                direction='nearest'
            )
            
            # Filtrer pour la fenêtre temporelle
            cutoff_date = merged_df['timestamp'].max() - timedelta(days=window_days)
            window_df = merged_df[merged_df['timestamp'] > cutoff_date]
            
            # Calculer les corrélations
            correlations = {}
            
            # Corrélation directe
            correlations['direct'] = window_df['price_change'].corr(window_df['sentiment_value'])
            
            # Corrélation avec décalage (sentiment précède le prix)
            for lag in [1, 3, 6, 12, 24]:
                window_df[f'sentiment_lag_{lag}'] = window_df['sentiment_value'].shift(lag)
                correlations[f'lag_{lag}h'] = window_df['price_change'].corr(window_df[f'sentiment_lag_{lag}'])
            
            # Corrélation avec avance (prix précède le sentiment)
            for lead in [1, 3, 6, 12, 24]:
                window_df[f'sentiment_lead_{lead}'] = window_df['sentiment_value'].shift(-lead)
                correlations[f'lead_{lead}h'] = window_df['price_change'].corr(window_df[f'sentiment_lead_{lead}'])
            
            # Trouver la meilleure corrélation
            best_corr = max(correlations.items(), key=lambda x: abs(x[1]))
            
            results[symbol] = {
                'correlations': correlations,
                'best_correlation': {
                    'type': best_corr[0],
                    'value': best_corr[1]
                },
                'interpretation': interpret_correlation(best_corr[0], best_corr[1]),
                'data_points': len(window_df),
                'window_days': window_days
            }
        
        return results
    except Exception as e:
        logger.error(f"Erreur lors du calcul des corrélations: {str(e)}")
        return {}

def interpret_correlation(corr_type, corr_value):
    """
    Interprète la corrélation
    
    Args:
        corr_type (str): Type de corrélation
        corr_value (float): Valeur de corrélation
        
    Returns:
        str: Interprétation de la corrélation
    """
    strength = ""
    if abs(corr_value) < 0.2:
        strength = "très faible"
    elif abs(corr_value) < 0.4:
        strength = "faible"
    elif abs(corr_value) < 0.6:
        strength = "modérée"
    elif abs(corr_value) < 0.8:
        strength = "forte"
    else:
        strength = "très forte"
    
    direction = "positive" if corr_value > 0 else "négative"
    
    if "lag" in corr_type:
        lag_hours = int(corr_type.split('_')[1].replace('h', ''))
        return f"Corrélation {strength} {direction} ({corr_value:.2f}) avec le sentiment précédant le prix de {lag_hours} heures"
    elif "lead" in corr_type:
        lead_hours = int(corr_type.split('_')[1].replace('h', ''))
        return f"Corrélation {strength} {direction} ({corr_value:.2f}) avec le prix précédant le sentiment de {lead_hours} heures"
    else:
        return f"Corrélation {strength} {direction} ({corr_value:.2f}) sans décalage temporel"

def generate_correlation_report(correlation_results):
    """
    Génère un rapport de corrélation
    
    Args:
        correlation_results (dict): Résultats de corrélation par symbole
        
    Returns:
        dict: Rapport de corrélation
    """
    try:
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "details": correlation_results
        }
        
        # Résumé global
        all_correlations = []
        for symbol, result in correlation_results.items():
            all_correlations.append(abs(result['best_correlation']['value']))
        
        if all_correlations:
            report["summary"]["average_correlation"] = sum(all_correlations) / len(all_correlations)
            report["summary"]["max_correlation_symbol"] = max(
                correlation_results.items(), 
                key=lambda x: abs(x[1]['best_correlation']['value'])
            )[0]
        
        # Recommandations basées sur les corrélations
        recommendations = []
        for symbol, result in correlation_results.items():
            corr_value = result['best_correlation']['value']
            corr_type = result['best_correlation']['type']
            
            if abs(corr_value) > 0.6:
                if "lag" in corr_type:
                    lag_hours = int(corr_type.split('_')[1].replace('h', ''))
                    if corr_value > 0:
                        recommendations.append(f"Surveiller le sentiment positif pour {symbol} comme indicateur avancé de hausse de prix ({lag_hours}h)")
                    else:
                        recommendations.append(f"Surveiller le sentiment négatif pour {symbol} comme indicateur avancé de baisse de prix ({lag_hours}h)")
        
        report["summary"]["recommendations"] = recommendations
        
        return report
    except Exception as e:
        logger.error(f"Erreur lors de la génération du rapport: {str(e)}")
        return {"error": str(e)}

def save_correlation_report(report):
    """
    Sauvegarde le rapport de corrélation
    
    Args:
        report (dict): Rapport de corrélation
    """
    try:
        # Créer le dossier si nécessaire
        os.makedirs('/home/crypto_bot/data', exist_ok=True)
        
        # Sauvegarder le rapport
        with open('/home/crypto_bot/data/correlation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info("Rapport de corrélation sauvegardé")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du rapport: {str(e)}")

def plot_correlation_heatmap(correlation_results):
    """
    Génère une heatmap des corrélations
    
    Args:
        correlation_results (dict): Résultats de corrélation par symbole
    """
    try:
        # Extraire les données pour la heatmap
        symbols = list(correlation_results.keys())
        correlation_types = ['direct', 'lag_1h', 'lag_3h', 'lag_6h', 'lag_12h', 'lag_24h']
        
        data = np.zeros((len(symbols), len(correlation_types)))
        
        for i, symbol in enumerate(symbols):
            for j, corr_type in enumerate(correlation_types):
                data[i, j] = correlation_results[symbol]['correlations'].get(corr_type, 0)
        
        # Créer la heatmap
        plt.figure(figsize=(12, 8))
        plt.imshow(data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        
        # Ajouter les labels
        plt.xticks(range(len(correlation_types)), correlation_types, rotation=45)
        plt.yticks(range(len(symbols)), symbols)
        
        # Ajouter les valeurs
        for i in range(len(symbols)):
            for j in range(len(correlation_types)):
                plt.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")
        
        plt.colorbar(label='Corrélation')
        plt.title('Corrélation entre sentiment et prix par crypto')
        plt.tight_layout()
        
        # Sauvegarder l'image
        plt.savefig('/home/crypto_bot/data/correlation_heatmap.png')
        logger.info("Heatmap de corrélation sauvegardée")
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la heatmap: {str(e)}")

def main():
    """
    Fonction principale
    """
    try:
        logger.info("Démarrage de l'analyse de corrélation")
        
        # Charger les données
        market_data, sentiment_data = load_data()
        
        if not market_data or not sentiment_data:
            logger.error("Données insuffisantes pour l'analyse")
            return
        
        # Prétraiter les données
        market_data_by_symbol = preprocess_market_data(market_data)
        sentiment_data_by_symbol = preprocess_sentiment_data(sentiment_data)
        
        # Calculer les corrélations
        correlation_results = calculate_correlation(market_data_by_symbol, sentiment_data_by_symbol)
        
        # Générer le rapport
        report = generate_correlation_report(correlation_results)
        
        # Sauvegarder le rapport
        save_correlation_report(report)
        
        # Générer la heatmap
        plot_correlation_heatmap(correlation_results)
        
        logger.info("Analyse de corrélation terminée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse de corrélation: {str(e)}")

if __name__ == "__main__":
    main()
