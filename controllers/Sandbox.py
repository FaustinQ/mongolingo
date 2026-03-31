import os
import json
from datetime import datetime
from bson import json_util
from bson import ObjectId

from db.DBConnection import DBConnection

from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/sandbox", tags=["Sandbox"])

@router.post("/reset")
async def reset_database():
    try:
        db_conn = DBConnection()
        collection = db_conn.get_collection("WaterPoints")
        
        # 1. On vide
        collection.delete_many({})
        
        # 2. On construit le chemin absolu vers le fichier
        # On part du dossier où se trouve Sandbox.py, on remonte d'un cran, et on va dans /data
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "..", "db", "waterpoints.json")
        
        if not os.path.exists(path):
            return {"success": False, "error": f"Fichier introuvable à l'adresse : {path}"}

        with open(path, "r", encoding="utf-8") as f:
            # On utilise json_util pour supporter les formats spécifiques Mongo ($date, $oid)
            data = json.loads(f.read(), object_hook=json_util.object_hook)
            
            if isinstance(data, list):
                if len(data) > 0:
                    collection.insert_many(data)
                else:
                    return {"success": False, "error": "Le fichier JSON est vide."}
            else:
                collection.insert_one(data)
                
        return {"success": True, "message": f"{len(data)} points d'eau restaurés !"}
    except Exception as e:
        # On renvoie l'erreur précise pour débugger
        return {"success": False, "error": str(e)}

@router.get("/export")
async def export_database():
    try:
        db_conn = DBConnection()
        collection = db_conn.get_collection("WaterPoints")
        
        # 1. Récupérer les données
        data = list(collection.find({}))
        
        # 2. Convertir en JSON String (avec support Date/ObjectId)
        # indent=2 rend le fichier joli à lire
        json_data = json_util.dumps(data, indent=2)
        
        # 3. Envoyer en tant que fichier texte/json
        return Response(
            content=json_data,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=export_waterpoints.json"
            }
        )
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/run")
async def run_custom_query(payload: dict):
    query_string = payload.get("query", "").strip()
    
    if not query_string:
        return {"success": False, "error": "La requête est vide."}

    try:
        # 1. Récupérer l'instance de la DB
        db_instance = DBConnection().get_db() 
        
        # 2. Préparer le contexte pour 'eval'
        # On définit 'db' pour que l'utilisateur puisse taper 'db.WaterPoints...'
        # On ajoute 'ObjectId' et 'datetime' pour les requêtes complexes
        context = {
            "db": db_instance,
            "ObjectId": ObjectId,
            "datetime": datetime
        }

        # 3. Exécution de la commande
        # ATTENTION : eval() exécute du code Python. 
        # Comme on utilise PyMongo, l'utilisateur doit utiliser la syntaxe Python :
        # .find() renvoie un curseur, il faut le transformer en liste.
        
        result = eval(query_string, {"__builtins__": {}}, context)

        # 4. Traitement du résultat selon le type (Curseur ou Action CRUD)
        if hasattr(result, "to_list"): # Si c'est un curseur (find)
            data = list(result.limit(50)) # On limite à 50 pour pas faire planter le navigateur
        elif hasattr(result, "inserted_id") or hasattr(result, "modified_count") or hasattr(result, "deleted_count"):
            # C'est une opération d'écriture (update, delete, insert)
            data = str(result.raw_result) if hasattr(result, "raw_result") else "Action effectuée avec succès"
        else:
            # Pour le reste (count_documents, etc.)
            data = result

        # 5. Conversion BSON -> JSON propre pour React
        clean_result = json.loads(json_util.dumps(data))
        
        return {"success": True, "result": clean_result}

    except Exception as e:
        return {"success": False, "error": str(e)}