import os
import sys
import joblib

# Définir le chemin absolu vers le fichier contenant les modèles et scalers
models_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../models/', 'best_model_lille.pkl')
)
# Définir le chemin absolu vers le fichier contenant les modèles et scalers
models_bordeaux_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../models/', 'best_model_bordeaux.pkl')
)

def load_model_a_lille():
    """
    Charge le modèle de régression pour les appartements à Lille.

    Returns:
        Un objet modèle (ex. : sklearn.ensemble.RandomForestRegressor).
    """
    return joblib.load(models_file)['model_a']


def load_model_a_bordeaux():
    """
    Charge le modèle de régression pour les appartements à bordeaux.

    Returns:
        Un objet modèle (ex. : sklearn.ensemble.RandomForestRegressor).
    """
    return joblib.load(models_bordeaux_file)['model_a']

def load_scaler_Xa_lille():
    """
    Charge le scaler des variables d'entrée pour les appartements à Lille.

    Returns:
        Un objet scaler (ex. : sklearn.preprocessing.StandardScaler).
    """
    return joblib.load(models_file)['scaler_Xa']

def load_scaler_ya_lille():
    """
    Charge le scaler des variables de sortie (prix) pour les appartements à Lille.

    Returns:
        Un objet scaler (ex. : sklearn.preprocessing.StandardScaler).
    """
    return joblib.load(models_file)['scaler_ya']

def load_model_m_lille():
    """
    Charge le modèle de régression pour les maisons à Lille.

    Returns:
        Un objet modèle (ex. : sklearn.ensemble.RandomForestRegressor).
    """
    return joblib.load(models_file)['model_m']

def load_model_m_bordeaux():
    """
    Charge le modèle de régression pour les maisons à bordeaux.

    Returns:
        Un objet modèle (ex. : sklearn.ensemble.RandomForestRegressor).
    """
    return joblib.load(models_bordeaux_file)['model_m']

def load_scaler_Xm_lille():
    """
    Charge le scaler des variables d'entrée pour les maisons à Lille.

    Returns:
        Un objet scaler (ex. : sklearn.preprocessing.StandardScaler).
    """
    return joblib.load(models_file)['scaler_Xm']

def load_scaler_ym_lille():
    """
    Charge le scaler des variables de sortie (prix) pour les maisons à Lille.

    Returns:
        Un objet scaler (ex. : sklearn.preprocessing.StandardScaler).
    """
    return joblib.load(models_file)['scaler_ym']
