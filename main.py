from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

# Imports existants
from controllers.waterpoints import router as water_router, init_waterpoints_dao
from controllers.questions import router as questions_router, init_questions_dao

# --- 1. AJOUTE L'IMPORT DU SANDBOX ---
from controllers.Sandbox import router as sandbox_router

from db.DBConnection import DBConnection

# Custom JSON encoder
def json_encoder_with_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return jsonable_encoder(obj)

app = FastAPI(title="API Mongolingo", json_encoder=json_encoder_with_objectid)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation
db = DBConnection()  
init_waterpoints_dao(db)
init_questions_dao(db) 

# --- 2. ENREGISTRE LES ROUTERS ---
app.include_router(water_router)
app.include_router(questions_router)
app.include_router(sandbox_router) # <--- CETTE LIGNE EST CRUCIALE POUR LE RESET