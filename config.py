import os

# Configuration and Paths
MODEL_PATH = os.getenv('MODEL_PATH', 'lead_scoring_model.pkl')
SCALER_PATH = os.getenv('SCALER_PATH', 'scaler.pkl')
FEATURES_PATH = os.getenv('FEATURES_PATH', 'model_features.pkl')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')
