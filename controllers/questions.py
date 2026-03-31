from fastapi import APIRouter, HTTPException, Depends
from models.Questions import Questions
from dao.QuestionsDAO import QuestionsDAO
from bson import ObjectId

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

# Variable globale pour le DAO (sera initialisée dans le main)
questions_dao = None

def init_questions_dao(db_connection):
    global questions_dao
    questions_dao = QuestionsDAO(db_connection)

@router.get("/random")
async def get_random_questions(limit: int = 5):
    """Récupère X questions au hasard pour le jeu"""
    try:
        # On utilise l'agrégation MongoDB pour la sélection aléatoire
        cursor = questions_dao.collection.aggregate([{"$sample": {"size": limit}}])
        
        # On formate chaque document via le DAO pour s'assurer que c'est propre
        questions_list = []

        for doc in cursor:
            q = questions_dao.get_question_by_id(doc.get("question_id"))
            if q:
                # On crée un dict manuellement avec les bons noms de clés
                q_dict = {
                    "question_id": q.question_id,
                    "choix_multiple": q.choix_multiple,
                    "enonce": q.enonce,
                    "difficulte": q.difficulte,
                    "propositions": q.propositions,
                    "solution": q.solution,
                    "explication": q.explication
                }
                questions_list.append(q_dict)
                
        return questions_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du tirage au sort : {str(e)}")

@router.get("/{question_id}")
async def get_one_question(question_id: str):
    """Récupère une question précise par son ID métier"""
    try:
        q = questions_dao.get_question_by_id(question_id)
        if not q:
            raise HTTPException(status_code=404, detail="Question introuvable")
        return q.__dict__
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))