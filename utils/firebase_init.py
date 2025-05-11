import firebase_admin
from firebase_admin import credentials
import os

# Global variable to track initialization
_firebase_initialized = False

def init_firebase():
    """Initialize Firebase Admin SDK only once"""
    global _firebase_initialized
    
    if not _firebase_initialized:
        try:
            # Get the absolute path to the firebase_config.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '..', 'firebase_config.json')
            
            cred = credentials.Certificate(config_path)
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
            print("✅ Firebase initialized successfully")
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            raise
