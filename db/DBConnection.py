from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class DBConnection:
    def __init__(self, test: bool = False):
        
        # Connexion au serveur MongoDB
        
        # Choisir l'URL MongoDB et le nom de la base selon le mode
        mongo_url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")

        # Connexion au serveur MongoDB
        self.client = MongoClient(mongo_url)

        # Accès à la base de données
        self.db = self.client[db_name]
        


    def get_collection(self, name):
        """Retourne la collection MongoDB par son nom"""
        return self.db[name]
    
    def get_db(self):
        """Retourne l'objet de la base de données (pour les cas où on veut faire du custom)"""
        return self.db

    def close(self):
        self.client.close()

