from bson.objectid import ObjectId

from models.WaterPoints import WaterPoints
from db.DBConnection import DBConnection
from datetime import datetime, time, date

import math
from bson import ObjectId

class WaterPointsDAO():

    def __init__(self, db: DBConnection):
        self.db = db
        self.collection = db.get_collection("WaterPoints")
    
    # --- MÉTHODE DE NETTOYAGE ADAPTÉE ---
    def _format_and_sanitize(self, doc):
        """Convertit le doc MongoDB en objet WaterPoints propre"""
        if not doc:
            return None
        # 1. Nettoyage récursif des NaN (toujours utile avant de créer l'objet)
        def clean(value):
            if isinstance(value, float) and math.isnan(value):
                return None
            if isinstance(value, list):
                return [clean(v) for v in value]
            if isinstance(value, dict):
                return {k: clean(v) for k, v in value.items()}
            return value
        clean_doc = clean(doc)
        
        # 2. Utilisation du modèle pour créer l'objet (valide les données)
        return WaterPoints.from_dict(clean_doc)
    
    
    

    def insert_waterpoints(self, wp_list):
        """Insère une liste d'objets WaterPoints"""
        if not wp_list: return

        documents = []
        for wp in wp_list:
            doc = wp.to_dict()
            if "id" in doc: del doc["id"]
            documents.append(doc)

        result = self.collection.insert_many(documents)
        for wp, oid in zip(wp_list, result.inserted_ids):
            wp.id = oid
            

    def create(self, wp: WaterPoints):
        """Insère un seul objet WaterPoints"""
        # On utilise to_dict du modèle, et on s'assure que _id n'est pas dedans
        doc = wp.to_dict()
        if "id" in doc: del doc["id"] # On laisse Mongo générer l'id
        result = self.collection.insert_one(doc)
        wp.id = result.inserted_id 
        return str(wp.id)

    def update(self, wp: WaterPoints):
        """Met à jour un WaterPoints"""
        if not wp.id: return False
        doc = wp.to_dict()
        # 1. On s'assure que l'ID est bien un ObjectId pour la requête
        try:
            db_id = ObjectId(wp.id) if not isinstance(wp.id, ObjectId) else wp.id
        except:
            return False
        # 2. On retire "id" du dictionnaire pour ne pas l'envoyer dans le $set
        if "id" in doc: del doc["id"]
        # 3. On lance l'update
        result = self.collection.update_one(
            {"_id": db_id}, 
            {"$set": doc}
        )
        return result.matched_count > 0

    def delete(self, wp_id: str) -> bool:
        """Supprime un WaterPoints par son ID"""
        result = self.collection.delete_one({"_id": ObjectId(wp_id)})
        return result.deleted_count > 0

    def findAll(self):
        """Récupère tous les WaterPoints en utilisant le formateur unique"""
        cursor = self.collection.find()
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findById(self, waterpoint_id: str):
        """ Récupère un waterpoint par son ID """
        return self.getById(id=waterpoint_id)

    def findInBounds(self, min_lat, max_lat, min_lon, max_lon):
            query = {
                "location": {
                    "$geoWithin": {
                        "$box": [
                            [min_lon, min_lat], # Coin bas-gauche [longitude, latitude]
                            [max_lon, max_lat]  # Coin haut-droit [longitude, latitude]
                        ]
                    }
                }
            }
            
            cursor = self.collection.find(query).limit(40)
            # Utilise ton formateur existant au lieu de WaterPoints(**doc)
            return [self._format_and_sanitize(doc) for doc in cursor]    

    def findByInsee5(self, insee_int):
        """Trouve les points d'eau par code INSEE5"""
        cursor = self.collection.find({"insee5": insee_int})
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findByTypeNature(self, type_nature: str):
        """Trouve les points d'eau par type de nature (ex: puit, source, etc.)"""
        cursor = self.collection.find({"type_nature": type_nature})
        return [self._format_and_sanitize(doc) for doc in cursor]



    def findNearby(self, lon: float, lat: float, max_dist_meters: float):
        """Trouve les points d'eau à proximité d'un point GPS"""
        self.collection.create_index([("location", "2dsphere")])
        query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": max_dist_meters
                }
            }
        }
        cursor = self.collection.find(query)
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByStatut(self, statut: str):
        """Trouve les points d'eau par statut (PUBLIC/PRIVE)""" 
        cursor = self.collection.find({"statut": statut})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByAccessibilite(self, accessibilite: str):
        """Trouve les points d'eau par accessibilité (C ou vide)""" 
        cursor = self.collection.find({"accessibilite": accessibilite}) 
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findByDisponibilite(self, disponibilite: str):
        """Trouve les points d'eau par disponibilité (DI ou IN)""" 
        cursor = self.collection.find({"disponibilite": disponibilite}) 
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findByUtilisateur(self, utilisateur: str):
        """Trouve les points d'eau par utilisateur"""
        cursor = self.collection.find({"utilisateur": utilisateur})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByNumeroPei(self, numero_pei: int):
        """Trouve les points d'eau par numéro de PEI""" 
        cursor = self.collection.find({"numero_pei": numero_pei})
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findByCartoRef(self, carto_ref: int):
        """Trouve les points d'eau par numéro de carte (carto_ref)""" 
        cursor = self.collection.find({"carto_ref": carto_ref})
        return [self._format_and_sanitize(doc) for doc in cursor]
        
    def findByDateMaj(self, date_obj: date):
        """Trouve les points d'eau par date de mise à jour"""
        try:
            start = datetime.combine(date_obj, time.min)
            end = datetime.combine(date_obj, time.max)
            start_str = start.isoformat()
            end_str = end.isoformat()
            print(f"DEBUG DAO: Cherche date_maj (string) entre {start_str} et {end_str}")
            query = {"date_maj": {"$gte": start_str, "$lte": end_str}}
            cursor = self.collection.find(query)
            return [self._format_and_sanitize(doc) for doc in cursor]
        except Exception as e:
            print(f"Erreur DAO (date_maj) : {e}")
            return []
    
    def findByDateCrea(self, date_obj: date):
        """Trouve les points d'eau par date de création"""
        try: 
            start = datetime.combine(date_obj, time.min)
            end = datetime.combine(date_obj, time.max)
            start_str = start.isoformat()
            end_str = end.isoformat()
            query = {"date_crea": {"$gte": start_str, "$lte": end_str}}
            cursor = self.collection.find(query)
            return [self._format_and_sanitize(doc) for doc in cursor]
        except Exception as e:
            print(f"Erreur DAO (date_crea) : {e}")
            return []
    
    def findByDerniereVerification(self, date_obj: date):
        """Trouve les points d'eau par date de dernière vérification"""
        try: 
            start = datetime.combine(date_obj, time.min)
            end = datetime.combine(date_obj, time.max)
            start_str = start.isoformat()
            end_str = end.isoformat()
            query = {"derniere_verification": {"$gte": start_str, "$lte": end_str}}
            cursor = self.collection.find(query)
            return [self._format_and_sanitize(doc) for doc in cursor]
        except Exception as e:
            print(f"Erreur DAO (derniere_verif) : {e}")
            return []
    
    def findByNbRaccordement(self, nb_raccordement: int):
        """Trouve les points d'eau par nombre de raccordement""" 
        cursor = self.collection.find({"nb_raccordement": nb_raccordement})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByVolEauMin(self,vol_eau_min: float):
        """Trouve les points d'eau par volume d'eau minimum"""
        cursor = self.collection.find({"vol_eau_min": {"$gte": vol_eau_min}})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByPressDebit(self, press_debit: float):
        """Trouve les points d'eau par pression et débit"""
        cursor = self.collection.find({"press_debit": {"$gte": press_debit}})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByDebit1Bar(self, debit_1_bar: float):
        """Trouve les points d'eau par débit 1 bar"""
        cursor = self.collection.find({"debit_1_bar": {"$gte": debit_1_bar}})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByTypePoint(self, type_point: str):
        """Trouve les points d'eau par type de point (CIVIL ou POMPIER)"""
        cursor = self.collection.find({"type_point": type_point})
        return [self._format_and_sanitize(doc) for doc in cursor]

    def findByTypeCivil(self, type_civil: str):
        """Trouve les points d'eau civil par type de point"""
        cursor = self.collection.find({"type_civil": type_civil})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def findByTailleCivil(self, taille_civil: str):
        """Trouve les points d'eau civil par taille de point"""
        cursor = self.collection.find({"taille_civil": taille_civil})
        return [self._format_and_sanitize(doc) for doc in cursor]
 

    def findByVerifieCivil(self, verifie_civil: bool):
        """Trouve les points d'eau civil en fonction de s'il sont vérifiés ou non"""
        cursor = self.collection.find({"verifie_civil": verifie_civil})
        return [self._format_and_sanitize(doc) for doc in cursor]
    
    def countWaterpoints(self):
        """Compte des points d'eau dans la base de données"""
        return self.collection.count_documents({})
    
    def deleteAll(self):
        """Supprime tous les points d'eau de la base"""
        result = self.collection.delete_many({})
        return result.deleted_count
    

