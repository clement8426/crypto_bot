import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/crypto_bot/logs/investment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('investment_tracker')

class InvestmentTracker:
    """Classe pour suivre et optimiser les investissements crypto"""
    
    def __init__(self, monthly_investment=50, data_dir='/home/crypto_bot/data'):
        """
        Initialise le tracker d'investissement
        
        Args:
            monthly_investment (float): Montant mensuel à investir en euros
            data_dir (str): Répertoire des données
        """
        self.monthly_investment = monthly_investment
        self.data_dir = data_dir
        self.market_data_file = os.path.join(data_dir, 'market_data.json')
        self.sentiment_data_file = os.path.join(data_dir, 'emotional_data.json')
        self.correlation_file = os.path.join(data_dir, 'correlation_report.json')
        self.portfolio_file = os.path.join(data_dir, 'portfolio.json')
        self.report_file = os.path.join(data_dir, 'investment_report.json')
        
        # Allocation de base (par défaut)
        self.base_allocation = {
            'BTC': 0.40,
            'ETH': 0.30,
            'SOL': 0.10,
            'ADA': 0.05,
            'BNB': 0.05,
            'DOT': 0.05,
            'XRP': 0.05
        }
        
        # Portefeuille actuel
        self.portfolio = self.load_portfolio()
    
    def load_portfolio(self):
        """
        Charge le portefeuille depuis le fichier JSON
        
        Returns:
            dict: Portefeuille actuel
        """
        try:
            if os.path.exists(self.portfolio_file):
                with open(self.portfolio_file, 'r') as f:
                    return json.load(f)
            else:
                # Créer un portefeuille vide
                portfolio = {
                    "total_invested": 0,
                    "current_value": 0,
                    "last_update": datetime.now().isoformat(),
                    "assets": {},
                    "history": []
                }
                return portfolio
        except Exception as e:
            logger.error(f"Erreur lors du chargement du portefeuille: {str(e)}")
            return {
                "total_invested": 0,
                "current_value": 0,
                "last_update": datetime.now().isoformat(),
                "assets": {},
                "history": []
            }
    
    def save_portfolio(self):
        """
        Sauvegarde le portefeuille dans un fichier JSON
        """
        try:
            os.makedirs(os.path.dirname(self.portfolio_file), exist_ok=True)
            with open(self.portfolio_file, 'w') as f:
                json.dump(self.portfolio, f, indent=2)
            logger.info("Portefeuille sauvegardé")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du portefeuille: {str(e)}")
    
    def load_market_data(self):
        """
        Charge les données de marché
        
        Returns:
            dict: Données de marché par symbole
        """
        try:
            with open(self.market_data_file, 'r') as f:
                market_data = json.load(f)
            
            # Organiser par symbole
            result = {}
            for item in market_data:
                symbol = item.get('symbol')
                if symbol not in result:
                    result[symbol] = []
                result[symbol].append(item)
            
            # Trier par timestamp et prendre le plus récent
            for symbol in result:
                result[symbol].sort(key=lambda x: x.get('timestamp', ''), reverse=True)
                result[symbol] = result[symbol][0]  # Garder seulement le plus récent
            
            return result
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données de marché: {str(e)}")
            return {}
    
    def load_correlation_data(self):
        """
        Charge les données de corrélation
        
        Returns:
            dict: Données de corrélation
        """
        try:
            if os.path.exists(self.correlation_file):
                with open(self.correlation_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données de corrélation: {str(e)}")
            return {}
    
    def generate_allocation(self):
        """
        Génère une allocation optimisée pour le portefeuille
        
        Returns:
            dict: Allocation optimisée
        """
        try:
            # Charger les données nécessaires
            market_data = self.load_market_data()
            correlation_data = self.load_correlation_data()
            
            # Partir de l'allocation de base
            allocation = self.base_allocation.copy()
            
            # Ajustements basés sur les signaux techniques
            adjustments = {}
            
            for symbol in allocation.keys():
                if symbol in market_data:
                    # Récupérer le signal technique
                    technical_signal = market_data[symbol].get('technical_signal', 'NEUTRAL')
                    
                    # Ajuster en fonction du signal
                    adjustment = 0
                    if technical_signal == 'BULLISH':
                        adjustment = 0.05
                    elif technical_signal == 'BULLISH_CAUTION':
                        adjustment = 0.02
                    elif technical_signal == 'BEARISH':
                        adjustment = -0.05
                    elif technical_signal == 'BEARISH_OPPORTUNITY':
                        adjustment = -0.02
                    
                    adjustments[symbol] = adjustment
            
            # Ajustements basés sur les corrélations
            if correlation_data and 'details' in correlation_data:
                for symbol, details in correlation_data['details'].items():
                    if symbol in allocation:
                        best_corr = details.get('best_correlation', {})
                        corr_value = best_corr.get('value', 0)
                        corr_type = best_corr.get('type', '')
                        
                        # Si forte corrélation positive avec décalage (sentiment précède prix)
                        if 'lag' in corr_type and corr_value > 0.5:
                            # Vérifier le sentiment récent
                            # Pour simplifier, on ajoute un petit bonus
                            adjustments[symbol] = adjustments.get(symbol, 0) + 0.02
            
            # Appliquer les ajustements
            for symbol, adjustment in adjustments.items():
                allocation[symbol] += adjustment
            
            # Normaliser pour avoir une somme de 1
            total = sum(allocation.values())
            normalized_allocation = {k: v / total for k, v in allocation.items()}
            
            # Calculer les montants en euros
            euro_allocation = {k: round(v * self.monthly_investment, 2) for k, v in normalized_allocation.items()}
            
            return {
                "base_allocation": self.base_allocation,
                "adjustments": adjustments,
                "normalized_allocation": normalized_allocation,
                "euro_allocation": euro_allocation,
                "total_investment": self.monthly_investment,
                "date": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'allocation: {str(e)}")
            # En cas d'erreur, retourner l'allocation de base
            euro_allocation = {k: round(v * self.monthly_investment, 2) for k, v in self.base_allocation.items()}
            return {
                "base_allocation": self.base_allocation,
                "adjustments": {},
                "normalized_allocation": self.base_allocation,
                "euro_allocation": euro_allocation,
                "total_investment": self.monthly_investment,
                "date": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def update_portfolio(self, allocation=None):
        """
        Met à jour le portefeuille avec une nouvelle allocation
        
        Args:
            allocation (dict, optional): Allocation à utiliser. Si None, génère une nouvelle allocation.
            
        Returns:
            dict: Portefeuille mis à jour
        """
        try:
            # Générer une allocation si non fournie
            if allocation is None:
                allocation = self.generate_allocation()
            
            # Charger les données de marché pour les prix actuels
            market_data = self.load_market_data()
            
            # Mettre à jour le portefeuille
            for symbol, amount in allocation['euro_allocation'].items():
                if symbol not in self.portfolio['assets']:
                    self.portfolio['assets'][symbol] = {
                        "total_invested": 0,
                        "quantity": 0
                    }
                
                # Calculer la quantité achetée
                price = market_data.get(symbol, {}).get('price', 0)
                if price > 0:
                    quantity = amount / price
                else:
                    quantity = 0
                
                # Mettre à jour l'actif
                self.portfolio['assets'][symbol]['total_invested'] += amount
                self.portfolio['assets'][symbol]['quantity'] += quantity
            
            # Mettre à jour le total investi
            self.portfolio['total_invested'] += self.monthly_investment
            
            # Calculer la valeur actuelle
            current_value = 0
            for symbol, asset in self.portfolio['assets'].items():
                price = market_data.get(symbol, {}).get('price', 0)
                asset_value = asset['quantity'] * price
                asset['current_value'] = asset_value
                current_value += asset_value
            
            self.portfolio['current_value'] = current_value
            
            # Ajouter à l'historique
            self.portfolio['history'].append({
                "date": datetime.now().isoformat(),
                "investment": self.monthly_investment,
                "allocation": allocation['normalized_allocation'],
                "total_invested": self.portfolio['total_invested'],
                "current_value": current_value
            })
            
            # Mettre à jour la date de dernière mise à jour
            self.portfolio['last_update'] = datetime.now().isoformat()
            
            # Sauvegarder le portefeuille
            self.save_portfolio()
            
            return self.portfolio
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du portefeuille: {str(e)}")
            return self.portfolio
    
    def generate_report(self):
        """
        Génère un rapport sur le portefeuille
        
        Returns:
            dict: Rapport du portefeuille
        """
        try:
            # Charger les données de marché pour les prix actuels
            market_data = self.load_market_data()
            
            # Calculer les performances
            performance = {}
            for symbol, asset in self.portfolio['assets'].items():
                if asset['total_invested'] > 0:
                    roi = (asset['current_value'] - asset['total_invested']) / asset['total_invested'] * 100
                    performance[symbol] = {
                        "total_invested": asset['total_invested'],
                        "current_value": asset['current_value'],
                        "quantity": asset['quantity'],
                        "current_price": market_data.get(symbol, {}).get('price', 0),
                        "roi_percent": roi
                    }
            
            # Calculer la performance globale
            total_roi = 0
            if self.portfolio['total_invested'] > 0:
                total_roi = (self.portfolio['current_value'] - self.portfolio['total_invested']) / self.portfolio['total_invested'] * 100
            
            # Générer le rapport
            report = {
                "date": datetime.now().isoformat(),
                "total_invested": self.portfolio['total_invested'],
                "current_value": self.portfolio['current_value'],
                "total_roi_percent": total_roi,
                "assets": performance,
                "monthly_investment": self.monthly_investment,
                "next_allocation": self.generate_allocation()
            }
            
            # Sauvegarder le rapport
            try:
                os.makedirs(os.path.dirname(self.report_file), exist_ok=True)
                with open(self.report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                logger.info("Rapport d'investissement sauvegardé")
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde du rapport: {str(e)}")
            
            return report
        except Exception as e:
            logger.error(f"Erreur lors de la génération du rapport: {str(e)}")
            return {
                "date": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def plot_portfolio_performance(self):
        """
        Génère un graphique de performance du portefeuille
        """
        try:
            if not self.portfolio['history']:
                logger.warning("Historique vide, impossible de générer le graphique")
                return
            
            # Préparer les données
            dates = []
            invested = []
            values = []
            
            for entry in self.portfolio['history']:
                dates.append(datetime.fromisoformat(entry['date']))
                invested.append(entry['total_invested'])
                values.append(entry['current_value'])
            
            # Créer le graphique
            plt.figure(figsize=(12, 6))
            
            plt.plot(dates, invested, 'b-', label='Total investi')
            plt.plot(dates, values, 'g-', label='Valeur actuelle')
            
            # Formater l'axe Y pour afficher les euros
            plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f} €'))
            
            plt.title('Performance du portefeuille crypto')
            plt.xlabel('Date')
            plt.ylabel('Valeur (EUR)')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            # Sauvegarder l'image
            plt.tight_layout()
            plt.savefig(os.path.join(self.data_dir, 'portfolio_performance.png'))
            logger.info("Graphique de performance sauvegardé")
            
            # Créer un graphique en camembert de la répartition actuelle
            self.plot_portfolio_allocation()
        except Exception as e:
            logger.error(f"Erreur lors de la génération du graphique: {str(e)}")
    
    def plot_portfolio_allocation(self):
        """
        Génère un graphique en camembert de la répartition du portefeuille
        """
        try:
            # Préparer les données
            labels = []
            values = []
            
            for symbol, asset in self.portfolio['assets'].items():
                if asset.get('current_value', 0) > 0:
                    labels.append(symbol)
                    values.append(asset['current_value'])
            
            if not values:
                logger.warning("Aucune valeur à afficher, impossible de générer le graphique")
                return
            
            # Créer le graphique
            plt.figure(figsize=(10, 8))
            
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            plt.title('Répartition du portefeuille crypto')
            
            # Sauvegarder l'image
            plt.tight_layout()
            plt.savefig(os.path.join(self.data_dir, 'portfolio_allocation.png'))
            logger.info("Graphique de répartition sauvegardé")
        except Exception as e:
            logger.error(f"Erreur lors de la génération du graphique de répartition: {str(e)}")

def main():
    """
    Fonction principale
    """
    try:
        logger.info("Démarrage du suivi d'investissement")
        
        # Initialiser le tracker
        tracker = InvestmentTracker()
        
        # Générer une allocation
        allocation = tracker.generate_allocation()
        logger.info(f"Allocation générée: {allocation['euro_allocation']}")
        
        # Mettre à jour le portefeuille
        tracker.update_portfolio(allocation)
        logger.info("Portefeuille mis à jour")
        
        # Générer le rapport
        report = tracker.generate_report()
        logger.info(f"Rapport généré: ROI total = {report['total_roi_percent']:.2f}%")
        
        # Générer les graphiques
        tracker.plot_portfolio_performance()
        
        logger.info("Suivi d'investissement terminé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du suivi d'investissement: {str(e)}")

if __name__ == "__main__":
    main()
