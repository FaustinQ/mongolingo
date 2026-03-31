from models.Questions import Questions
from db.DBConnection import DBConnection

class QuestionsDAO:
    def __init__(self, db: DBConnection):
        self.db = db
        self.collection = db.get_collection("Questions")
    
    def insert_question(self, question: Questions):
        """Insère une question dans la collection MongoDB"""
        doc = {
            "question_id": question.question_id,
            "choix_multiple": question.choix_multiple,
            "enonce": question.enonce,
            "difficulte": question.difficulte,
            "propositions": question.propositions,
            "solution": question.solution,
            "explication": question.explication
        }
        result = self.collection.insert_one(doc)
        return str(result.inserted_id)
    
    def get_question_by_id(self, question_id: str):
        """Récupère une question par son ID"""
        doc = self.collection.find_one({"question_id": question_id})
        if doc:
            return Questions(
                question_id=doc.get("question_id"),
                choix_multiple=doc.get("choix_multiple"),
                enonce=doc.get("enonce"),
                difficulte=doc.get("difficulte"),
                propositions=doc.get("propositions"),
                solution=doc.get("solution"),
                explication=doc.get("explication")
            )
        return None