from datetime import date, datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from db import DBConnection
from models.WaterPoints import WaterPoints
from dao.WaterPointsDAO import WaterPointsDAO
from bson import ObjectId


# Routeur
router = APIRouter(
    prefix="/waterpoints",
    tags=["WaterPoints"]
)

# Initialisation de la connexion à la BDD 
waterpoints_dao = None

# Fonction d'initialisation de la connexion à la base 
def init_waterpoints_dao(db_connection):
    global waterpoints_dao
    waterpoints_dao = WaterPointsDAO(db_connection)

# Schéma Pydantic pour la création d'utilisateur
class WaterPointCreate(BaseModel):
    # Sécurité pour les booléens (True ne sera plus transformé en 1)
    model_config = ConfigDict(strict=True)

    longitude: float
    latitude: float
    date_crea: date | None = None
    date_maj: date | None = None
    utilisateur: str | None = None
    carto_ref: int | None = None
    statut: str | None = None
    press_debit: float | None = None
    debit_1_bar: float | None = None
    numero_pei: int | None = None
    insee5: int | None = None
    type_nature: str | None = None
    vol_eau_min: float | None = None
    accessibilite: str | None = None
    disponibilite: str | None = None
    derniere_verification: date | None = None
    nb_raccordement: int | None = None
    type_point: str | None = None
    type_civil: str | None = None
    taille_civil: str | None = None
    acces_public: str | None = None
    verifie_civil: bool | None = None

    @field_validator('date_crea', 'date_maj', 'derniere_verification', mode='before')
    @classmethod
    def validate_dates_custom(cls, v):
        # 1. Gestion du vide
        if v == "" or v is None:
            return None
        # 2. Si c'est déjà un objet date, on le laisse passer
        if isinstance(v, date):
            return v
        # 3. Si c'est du texte, on utilise la méthode standard de Python
        if isinstance(v, str):
            try:
                # fromisoformat transforme "2024-01-01" en objet date
                return date.fromisoformat(v)
            except Exception:
                # Si le format est mauvais (ex: "hier"), on renvoie tel quel
                # Pydantic affichera l'erreur de validation normale
                return v
        return v

@router.post("/create")
async def create_waterpoint(waterpoint: WaterPointCreate):
    try:
        # Créer l'objet WaterPoints
        new_waterpoint = WaterPoints(
            longitude=waterpoint.longitude,
            latitude=waterpoint.latitude,
            date_crea=waterpoint.date_crea,
            date_maj=waterpoint.date_maj,
            utilisateur=waterpoint.utilisateur,
            carto_ref=waterpoint.carto_ref,
            statut=waterpoint.statut,
            press_debit=waterpoint.press_debit,
            debit_1_bar=waterpoint.debit_1_bar,
            numero_pei=waterpoint.numero_pei,
            insee5=waterpoint.insee5,
            type_nature=waterpoint.type_nature,
            vol_eau_min=waterpoint.vol_eau_min,
            accessibilite=waterpoint.accessibilite,
            disponibilite=waterpoint.disponibilite,
            derniere_verification=waterpoint.derniere_verification,
            nb_raccordement=waterpoint.nb_raccordement,
            type_point=waterpoint.type_point,
            type_civil=waterpoint.type_civil,
            taille_civil=waterpoint.taille_civil,
            acces_public=waterpoint.acces_public,
            verifie_civil=waterpoint.verifie_civil
        )

        # On récupère l'ID généré par le DAO
        generated_id = waterpoints_dao.create(new_waterpoint)

        return {
            "id": str(generated_id),
            "message": "Point d'eau créé avec succès !"
        }

    except Exception as e:
        print(f"ERREUR SERVEUR: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la création")

@router.delete("/{waterpoint_id}")
async def delete_waterpoint(waterpoint_id: str):
    try:
        if not ObjectId.is_valid(waterpoint_id):
            raise HTTPException(status_code=404, detail="Format d'ID invalide ou point inexistant")

        existing = waterpoints_dao.findById(waterpoint_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Point d'eau non trouvé")

        result = waterpoints_dao.delete(waterpoint_id)
        if not result:
            raise HTTPException(status_code=404, detail="Point d'eau non trouvé")
        return {"message": "Point d'eau supprimé avec succès !"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bounds")
async def get_waterpoints_by_bounds(min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    try:
        # On appelle le DAO pour filtrer les points dans le rectangle
        waterpoints = waterpoints_dao.findInBounds(min_lat, max_lat, min_lon, max_lon)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        print(f"ERREUR BOUNDS: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération par zone")

@router.get("/nearby")
async def get_nearby_waterpoints(longitude: float, latitude: float, radius: float):
    # On valide NOUS-MÊMES les données avant d'envoyer à MongoDB
    if not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Longitude invalide (-180 à 180)")
    if not (-90 <= latitude <= 90):
        raise HTTPException(status_code=400, detail="Latitude invalide (-90 à 90)")
    if radius < 0:
        raise HTTPException(status_code=400, detail="Le rayon doit être positif")
    try:
        waterpoints = waterpoints_dao.findNearby(longitude, latitude, radius)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        # Si malgré nos tests ça plante encore, là c'est une erreur 500
        print(f"ERREUR INCONNUE : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la recherche")



@router.get("/{waterpoint_id}")
async def get_waterpoint(waterpoint_id: str):
    try:
        if not ObjectId.is_valid(waterpoint_id):
            raise HTTPException(status_code=404, detail="Format d'ID invalide")
        waterpoint = waterpoints_dao.findById(waterpoint_id)
        if not waterpoint:
            raise HTTPException(status_code=404, detail="Point d'eau non trouvé")
        return waterpoint.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur GET: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/")
async def get_all_waterpoints():
    try:
        waterpoints = waterpoints_dao.findAll()

        print(f"DEBUG: {len(waterpoints)} points d'eau récupérés.")
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        print(f"ERREUR SERVEUR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{waterpoint_id}")
async def update_waterpoint(waterpoint_id: str, waterpoint: WaterPointCreate):
    try:
        if not ObjectId.is_valid(waterpoint_id):
            raise HTTPException(status_code=400, detail="Format d'ID invalide")

        existing = waterpoints_dao.findById(waterpoint_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Point d'eau non trouvé")

        updated_waterpoint = WaterPoints(
            longitude=waterpoint.longitude,
            latitude=waterpoint.latitude,
            date_crea=waterpoint.date_crea,
            date_maj=waterpoint.date_maj,
            utilisateur=waterpoint.utilisateur,
            carto_ref=waterpoint.carto_ref,
            statut=waterpoint.statut,
            press_debit=waterpoint.press_debit,
            debit_1_bar=waterpoint.debit_1_bar,
            numero_pei=waterpoint.numero_pei,
            insee5=waterpoint.insee5,
            type_nature=waterpoint.type_nature,
            vol_eau_min=waterpoint.vol_eau_min,
            accessibilite=waterpoint.accessibilite,
            disponibilite=waterpoint.disponibilite,
            derniere_verification=waterpoint.derniere_verification,
            nb_raccordement=waterpoint.nb_raccordement,
            type_point=waterpoint.type_point,
            type_civil=waterpoint.type_civil,
            taille_civil=waterpoint.taille_civil,
            acces_public=waterpoint.acces_public,
            verifie_civil=waterpoint.verifie_civil
        )
        updated_waterpoint._id = ObjectId(waterpoint_id)
        success = waterpoints_dao.update(updated_waterpoint)
        if not success:
            raise HTTPException(status_code=404, detail="Point d'eau non trouvé")   
        return {"message": "Point d'eau mis à jour avec succès !"}
    except HTTPException:
        raise
    except ValueError as e:
        print(f"ERREUR DE VALIDATION: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"DEBUG CRASH UPDATE: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by_insee/{insee5}")
async def get_waterpoints_by_insee(insee5: str):
    if len(insee5) != 5:
        raise HTTPException(status_code=400, detail="Le code INSEE doit faire 5 caractères")
    try:
        insee_int = int(insee5) 
        waterpoints = waterpoints_dao.findByInsee5(insee_int)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=400, detail="Le code INSEE doit être un nombre.")


@router.get("/by_type/{type_nature}")
async def get_waterpoints_by_type(type_nature: str):
    if not type_nature.strip() and type_nature.lower() != "null":
        raise HTTPException(status_code=400, detail="Le type de nature ne peut pas être vide.")
    try:
        waterpoints = waterpoints_dao.findByTypeNature(type_nature)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_statut/{statut}")
async def get_waterpoints_by_statut(statut: str):
    s = statut.strip().upper()
    if s not in ["PUBLIC", "PRIVE"]: 
        raise HTTPException(status_code=400, detail="Le statut doit être 'PUBLIC' ou 'PRIVE'.")
    try:
        waterpoints = waterpoints_dao.findByStatut(s)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_accessibilite/{accessibilite}")
async def get_waterpoints_by_accessibilite(accessibilite: str):
    val = accessibilite.strip().lower()
    if val == "null":
        recherche = None
    elif val == "c":
        recherche = "C"
    else:
        raise HTTPException(status_code=400, detail="L'accessibilité doit être 'C' ou 'null'.")
    try:
        waterpoints = waterpoints_dao.findByAccessibilite(recherche)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_disponibilite/{disponibilite}")
async def get_waterpoints_by_disponibilite(disponibilite: str):
    val = disponibilite.strip().lower()
    if val in ["in", "di"]: 
        recherche = val.upper()
    else:
        raise HTTPException(status_code=400, detail="La disponibilité doit être 'DI' ou 'IN'.")
    try:
        waterpoints = waterpoints_dao.findByDisponibilite(recherche)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_utilisateur/{utilisateur}")
async def get_waterpoints_by_utilisateur(utilisateur: str):
    user_clean = utilisateur.strip()
    if not utilisateur.strip():
        raise HTTPException(status_code=400, detail="Le nom d'utilisateur ne peut pas être vide.")

    try:
        waterpoints = waterpoints_dao.findByUtilisateur(user_clean)
        if not waterpoints:
            return []
        return [wp.to_dict() for wp in waterpoints]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_numero_pei/{numero_pei}")
async def get_waterpoints_by_numero_pei(numero_pei: str):
    try:
        num = int(numero_pei)
        waterpoints = waterpoints_dao.findByNumeroPei(num)
        if  not waterpoints: 
            raise HTTPException(status_code=404, detail=f"Aucun point d'eau trouvé pour le numéro PEI '{num}'." )
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=400, detail="Le numéro PEI doit être un nombre entier.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_carto_ref/{carto_ref}")
async def get_waterpoints_by_carto_ref(carto_ref: str): 
    ref_clean = carto_ref.strip()
    if not ref_clean:
        raise HTTPException(status_code=422, detail="Le numéro de carte ne peut pas être vide.")
    if ref_clean.startswith('0'):
        raise HTTPException(status_code=422, detail="Le numéro de carte ne peut pas commencer par 0.")
    try:
        num = int(ref_clean)
        waterpoints = waterpoints_dao.findByCartoRef(num)
        if not waterpoints: 
            raise HTTPException(status_code=404, detail=f"Aucun point d'eau trouvé pour le numéro de carte '{num}'.")
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="Le numéro de carte doit être un nombre entier.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_date_maj/{date_maj}")
async def get_waterpoints_by_date_maj(date_maj: str):
    date_clean = date_maj.strip()
    if not date_clean:
        raise HTTPException(status_code=422, detail="La date de mise à jour ne peut pas être vide.")
    try:
        obj_date = datetime.strptime(date_clean, "%Y-%m-%d").date() 
        waterpoints = waterpoints_dao.findByDateMaj(obj_date)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="La date de mise à jour n'est pas au format YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_date_crea/{date_crea}")
async def get_waterpoints_by_date_crea(date_crea: str):
    date_clean = date_crea.strip()
    if not date_clean:
        raise HTTPException(status_code=422, detail="La date de création ne peut pas être vide.")
    try:
        obj_date = datetime.strptime(date_clean, "%Y-%m-%d").date()
        waterpoints = waterpoints_dao.findByDateCrea(obj_date)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="La date de création n'est pas au format YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_derniere_verification/{derniere_verification}")
async def get_waterpoints_by_derniere_verification(derniere_verification: str):
    date_clean = derniere_verification.strip()
    if not date_clean:
        raise HTTPException(status_code=422, detail="La dernière vérification n'est pas au format YYYY-MM-DD.")
    try:
        obj_date = datetime.strptime(date_clean, "%Y-%m-%d").date()
        waterpoints = waterpoints_dao.findByDerniereVerification(obj_date)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="La dernière vérification n'est pas au format YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_nb_raccordement/{nb_raccordement}")
async def get_waterpoints_by_nb_raccordement(nb_raccordement: str):
    nb = nb_raccordement.strip()
    if not nb:
        raise HTTPException(status_code=422, detail="Le nombre de raccordement ne peut pas être vide.")
    if nb.startswith('0') and len(nb) > 1:
        raise HTTPException(status_code=422, detail="Le nombre de raccordement ne peut pas commencer par 0.")
    try:
        num = int(nb)
        if num < 0:
            raise HTTPException(status_code=422, detail="Le nombre de raccordement ne peut pas être négatif.")
        waterpoints = waterpoints_dao.findByNbRaccordement(num)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="Le nombre de raccordement doit être un nombre entier")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/by_vol_eau_min/{vol_eau_min}")
async def get_waterpoints_by_vol_eau_min(vol_eau_min: str):
    vol = vol_eau_min.replace(" ", "").replace(",", ".").strip()
    if not vol: 
        raise HTTPException(status_code=422, detail="Le volume ne peut pas être vide.")
    try:
        vol = float(vol)
        if vol < 0 :
            raise HTTPException(status_code=422, detail="Le volume ne peut pas être négatif.")
        waterpoints = waterpoints_dao.findByVolEauMin(vol)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError:
        raise HTTPException(status_code=422, detail="Le volume doit être un nombre valide.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_press_debit/{press_debit}")
async def get_waterpoints_by_press_debit(press_debit: str):
    press = press_debit.replace(" ", "").replace(",", ".").strip()
    if not press: 
        raise HTTPException(status_code=422, detail="La pression ne peut pas être vide.")
    try:
        press = float(press)
    except ValueError:
        raise HTTPException(status_code=422, detail="La pression doit être un nombre valide.")
    if press < 0 :
        raise HTTPException(status_code=422, detail="La pression ne peut pas être négative.")
    try:
        waterpoints = waterpoints_dao.findByPressDebit(press)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_debit_1_bar/{debit_1_bar}")
async def get_waterpoints_by_debit_1_bar(debit_1_bar: str):
    deb = debit_1_bar.replace(" ", "").replace(",", ".").strip()
    if not deb: 
        raise HTTPException(status_code=422, detail="Le débit 1 bar ne peut pas être vide.")
    try:
        deb = float(deb)
    except ValueError:
        raise HTTPException(status_code=422, detail="Le débit 1 bar doit être un nombre valide.")
    if deb < 0 :
        raise HTTPException(status_code=422, detail="Le débit 1 bar ne peut pas être négative.")
    try:
        waterpoints = waterpoints_dao.findByDebit1Bar(deb)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/by_type_point/{type_point}")
async def get_waterpoints_by_type_point(type_point: str):
    t = type_point.strip().upper()
    if t not in ["CIVIL", "POMPIER"]:
        raise HTTPException(status_code=422, detail="Le type_point doit être 'CIVIL' ou 'POMPIER'.")
    try:
        waterpoints = waterpoints_dao.findByTypePoint(type_point)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/by_type_civil/{type_civil}")
async def get_waterpoints_by_type_civil(type_civil: str):
    if not type_civil.strip() and type_civil.lower() != "null":
        raise HTTPException(status_code=400, detail="Le type_civil ne peut pas être vide.")
    try:
        waterpoints = waterpoints_dao.findByTypeCivil(type_civil)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/by_taille_civil/{taille_civil}")
async def get_waterpoints_by_taille_civil(taille_civil: str):
    t = taille_civil.strip().lower()
    if t not in ["petit", "moyen", "grand"]:
        raise HTTPException(status_code=422, detail="La taille_civil doit être 'petit', 'moyen' ou 'grand'.")
    try:
        waterpoints = waterpoints_dao.findByTailleCivil(taille_civil)
        return [wp.to_dict() for wp in waterpoints]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_verifie_civil/{verifie_civil}")
async def get_waterpoints_by_verifie_civil(verifie_civil: str):
    val = verifie_civil.strip().lower()
    if val == "true":
        boolean_val = True
    elif val == "false":
        boolean_val = False
    else:
        raise HTTPException(status_code=400, detail="Doit être 'true' ou 'false'")
    try:
        waterpoints = waterpoints_dao.findByVerifieCivil(boolean_val)
        return [wp.to_dict() for wp in waterpoints]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/count")
async def count_waterpoints():
    try:
        count = waterpoints_dao.countWaterpoints()
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/all")
async def delete_all():
    try:
        nb_supp = waterpoints_dao.deleteAll()
        print(f"DEBUG: {nb_supp} points d'eau supprimés.")
        return nb_supp
    except Exception as e:
        print(f"ERREUR SERVEUR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reset")
async def reset_database():
    try:
        db = DBConnection().get_collection("WaterPoints")
        db.delete_many({}) # On vide tout
        
        # On recharge depuis ton fichier local (ex: data/waterpoints.json)
        import json
        with open('data/waterpoints_original.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Si le JSON est une liste d'objets
            db.insert_many(data)
            
        return {"success": True, "message": "Base réinitialisée avec les données du Morbihan !"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

