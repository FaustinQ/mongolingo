class Questions:

    def __init__(self, 
                 question_id=None,
                 choix_multiple=None, 
                 enonce=None,
                 difficulte=None,
                 propositions=None,
                 solution=None,
                 explication=None,):
        
        self._id = question_id
        self._choix_multiple = choix_multiple
        self._enonce = enonce
        self._difficulte = difficulte
        self._propositions = propositions
        self._solution = solution
        self._explication = explication

    @property
    def question_id(self):
        return self._id
    
    @question_id.setter
    def question_id(self, value):
        if value is None or not isinstance(value, str):
            raise ValueError("question_id doit être une chaîne de caractères ou None.")
        self._id = value

    @property
    def choix_multiple(self):
        return self._choix_multiple
    
    @choix_multiple.setter
    def choix_multiple(self, value):
        if value is None or not isinstance(value, bool):
            raise ValueError("choix_multiple doit être un booléen ou None.")
        self._choix_multiple = value

    @property
    def enonce(self):
        return self._enonce
    
    @enonce.setter
    def enonce(self, value):
        if value is None or not isinstance(value, str):
            raise ValueError("enonce doit être une chaîne de caractères ou None.")
        self._enonce = value

    @property
    def difficulte(self):
        return self._difficulte
    
    @difficulte.setter
    def difficulte(self, value):
        if value is None or value not in ("Facile", "Intermédiaire", "Complexe", "Expert"):
            raise ValueError("difficulte doit être l'une de ces valeurs : 'Facile', 'Intermédiaire', 'Complexe', 'Expert'.")
        self._difficulte = value

    @property
    def propositions(self):
        return self._propositions
    
    @propositions.setter
    def propositions(self, value):
        if value is None or not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError("propositions doit être une liste de chaînes de caractères ou None.")
        self._propositions = value

    @property
    def solution(self):
        return self._solution
    
    @solution.setter
    def solution(self, value):
        if value is None or not isinstance(value, str):
            raise ValueError("solution doit être une chaîne de caractères ou None.")
        self._solution = value

    @property
    def explication(self):
        return self._explication
    
    @explication.setter
    def explication(self, value):
        if value is None or not isinstance(value, str):
            raise ValueError("explication doit être une chaîne de caractères ou None.")
        self._explication = value
        