import datetime
from bson import ObjectId

class WaterPoints:

    def __init__(self, 
                 id=None,
                 longitude=None, 
                 latitude=None,
                 location=None,
                 date_crea=None,
                 date_maj=None,
                 utilisateur=None,
                 carto_ref=None,
                 statut=None,
                 press_debit=None,
                 debit_1_bar=None,
                 numero_pei=None,
                 insee5=None,
                 type_nature=None,
                 vol_eau_min=None,
                 accessibilite=None,
                 disponibilite=None,
                 derniere_verification=None, 
                 nb_raccordement=None,
                 type_point=None,
                 type_civil=None,
                 taille_civil=None,
                 acces_public=None,
                 verifie_civil=None):
        self._id = id

        self._longitude = None
        self._latitude = None

        if location is not None:
            longitude = location["coordinates"][0]
            latitude = location["coordinates"][1]

        self.longitude = longitude
        self.latitude = latitude
        self.date_crea = date_crea
        self.date_maj = date_maj
        self.utilisateur = utilisateur
        self.carto_ref = carto_ref
        self.statut = statut
        self.press_debit = press_debit
        self.debit_1_bar = debit_1_bar
        self.numero_pei = numero_pei
        self.insee5 = insee5
        self.type_nature = type_nature
        self.vol_eau_min = vol_eau_min
        self.accessibilite = accessibilite
        self.disponibilite = disponibilite
        self.derniere_verification = derniere_verification
        self.nb_raccordement = nb_raccordement
        self.type_point = type_point
        self.type_civil = type_civil
        self.taille_civil = taille_civil
        self.acces_public = acces_public
        self.verifie_civil = verifie_civil


    # ------- id -------
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, ObjectId):
            try:
                value = ObjectId(value)
            except Exception:
                raise ValueError("id doit être un ObjectId valide ou None")
        self._id = value


    # ------- latitude -------
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if isinstance(value, bool):
            raise ValueError("La latitude ne peut pas être un booléen.")
        
        if value is None or not isinstance(value, (int, float)):
            raise ValueError("La latitude doit être un nombre.")

        if not (-90 <= value <= 90):
            raise ValueError("La latitude doit être comprise entre -90 et 90.")
        self._latitude = value
        self._update_location()


    # ------- longitude -------
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if isinstance(value, bool):
            raise ValueError("La longitude ne peut pas être un booléen.")
        
        if value is None or not isinstance(value, (int, float)):
            raise ValueError("La longitude doit être un nombre.")

        if not (-180 <= value <= 180):
            raise ValueError("La longitude doit être entre -180 et 180.")
        self._longitude = value
        self._update_location()

    # ------- mise à jour de la localisation -------
    def _update_location(self):
        if hasattr(self, "_longitude") and hasattr(self, "_latitude"):
            self.location = {
                "type": "Point",
                "coordinates": [self._longitude, self._latitude]
            }


    # ------- création des objet datetime -------
    def _validate_date(self, value, field_name):
        # 1. Gestion des vides
        if value is None or value == "":
            return None
        # 2. Si c'est déjà un datetime, on le garde
        if isinstance(value, datetime.datetime):
            return value
        # 3. Si c'est un objet date (sans l'heure), on le convertit en datetime
        if isinstance(value, datetime.date):
            return datetime.datetime.combine(value, datetime.time.min)
        # 4. Si c'est une chaîne de caractères (le cas qui pose problème)
        if isinstance(value, str):
            try:
                # On essaie d'abord le format ISO (ex: 2024-01-01T10:00:00)
                return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                try:
                    # Sinon on essaie le format simple YYYY-MM-DD
                    return datetime.datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"Le format de date pour {field_name} est invalide ('{value}'). Utilisez YYYY-MM-DD.")
        # 5. Si c'est un autre type, erreur
        raise ValueError(f"{field_name} doit être un datetime, une date ou une chaîne valide.")


    # ------- date_crea -------
    @property
    def date_crea(self):
        return self._date_crea

    @date_crea.setter
    def date_crea(self, value): 
        self._date_crea = self._validate_date(value, "date_crea")


    # ------- date_maj -------
    @property
    def date_maj(self):
        return self._date_maj

    @date_maj.setter
    def date_maj(self, value):
        self._date_maj = self._validate_date(value, "date_maj")


    # ------- utilisateur -------
    @property
    def utilisateur(self):
        return self._utilisateur

    @utilisateur.setter
    def utilisateur(self, value):
        if value is not None and (not isinstance(value, str) or value.strip() == ""):
            raise ValueError("Utilisateur doit être une chaîne non vide.")
        self._utilisateur = value


    # ------- carto_ref -------
    @property
    def carto_ref(self):
        return self._carto_ref

    @carto_ref.setter
    def carto_ref(self, value):
        if isinstance(value, bool): 
            raise ValueError("carto_ref ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("carto_ref doit être un entier positif ou None.")
        self._carto_ref = value


    # ------- statut -------
    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, value):
        if value not in ["PUBLIC", "PRIVE"]:
            raise ValueError("statut doit être 'PUBLIC' ou 'PRIVE'.")
        self._statut = value


    # ------- press_debit -------
    @property
    def press_debit(self):
        return self._press_debit

    @press_debit.setter
    def press_debit(self, value):
        if isinstance(value, bool): 
            raise ValueError("press_debit ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, (int, float)) or value < 0):
            raise ValueError("press_debit doit être un nombre positif.")
        self._press_debit = value


    # ------- debit_1_bar -------
    @property
    def debit_1_bar(self):
        return self._debit_1_bar

    @debit_1_bar.setter
    def debit_1_bar(self, value):
        if isinstance(value, bool): 
            raise ValueError("debit_1_bar ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, (int, float)) or value < 0):
            raise ValueError("debit_1_bar doit être un nombre positif.")
        self._debit_1_bar = value


    # ------- numero_pei -------
    @property
    def numero_pei(self):
        return self._numero_pei

    @numero_pei.setter
    def numero_pei(self, value):
        if isinstance(value, bool): 
            raise ValueError("numero_pei ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("numero_pei doit être un entier positif ou None.")
        self._numero_pei = value


    # ------- insee5 -------
    @property
    def insee5(self):
        return self._insee5

    @insee5.setter
    def insee5(self, value):
        if isinstance(value, bool): 
            raise ValueError("insee5 ne peut pas être un booléen.")        
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("insee5 doit être un entier positif ou None.")
        self._insee5 = value


    # ------- type_nature -------
    @property
    def type_nature(self):
        return self._type_nature

    @type_nature.setter
    def type_nature(self, value):
        if value is not None and (not isinstance(value, str) or value.strip() == ""):
            raise ValueError("type_nature doit être une chaîne non vide.")
        self._type_nature = value


    # ------- vol_eau_min -------
    @property
    def vol_eau_min(self):
        return self._vol_eau_min

    @vol_eau_min.setter
    def vol_eau_min(self, value):
        if isinstance(value, bool): 
            raise ValueError("vol_eau_min ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, (int, float)) or value < 0):
            raise ValueError("vol_eau_min doit être un nombre positif.")
        self._vol_eau_min = value


    # ------- accessibilite -------
    @property
    def accessibilite(self):
        return self._accessibilite

    @accessibilite.setter
    def accessibilite(self, value):
        if value is not None and value != "C":
            raise ValueError("accessibilite doit être 'C' ou None.")
        self._accessibilite = value


    # ------- disponibilite -------
    @property
    def disponibilite(self):
        return self._disponibilite

    @disponibilite.setter
    def disponibilite(self, value):
        if value not in ["IN", "DI"]:
            raise ValueError("disponibilite doit être 'IN' ou 'DI'.")
        self._disponibilite = value


    # ------- derniere_verification -------
    @property
    def derniere_verification(self):
        return self._derniere_verification

    @derniere_verification.setter
    def derniere_verification(self, value):
        self._derniere_verification = self._validate_date(value, "derniere_verification")


    # ------- nb_raccordement -------
    @property
    def nb_raccordement(self):
        return self._nb_raccordement

    @nb_raccordement.setter
    def nb_raccordement(self, value):
        if isinstance(value, bool): 
            raise ValueError("nb_raccordement ne peut pas être un booléen.")
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError("nb_raccordement doit être un entier positif.")
        self._nb_raccordement = value

    def __str__(self):
        return f"WaterPoints(id={self.id}, longitude={self.longitude}, latitude={self.latitude}, date_crea={self.date_crea}, date_maj={self.date_maj}, utilisateur='{self.utilisateur}', carto_ref={self.carto_ref}, statut='{self.statut}', press_debit={self.press_debit}, debit_1_bar={self.debit_1_bar}, numero_pei={self.numero_pei}, insee5={self.insee5}, type_nature='{self.type_nature}', vol_eau_min={self.vol_eau_min}, accessibilite='{self.accessibilite}', disponibilite={self.disponibilite}, derniere_verification={self.derniere_verification}, nb_raccordement={self.nb_raccordement},  type_point={self.type_point}, type_civil={self.type_civil}, taille_civil={self.taille_civil}, acces_public={self.acces_public})"


    # ------- type_point -------
    @property
    def type_point(self):
        return self._type_point
    
    @type_point.setter
    def type_point(self, value):
        if value is None:
            self._type_point = None
            return
        if not isinstance(value, str):
            raise ValueError("type_point doit être une chaine de caractères ('CIVIL' ou 'POMPIER')")
        if value not in ["CIVIL", "POMPIER"]:
            raise ValueError("type_point doit être 'CIVIL' ou 'POMPIER'.")
        self._type_point = value
    

    # ------- type_civil -------
    @property
    def type_civil(self):
        return self._type_civil
    
    @type_civil.setter
    def type_civil(self, value):
        if value is None:
            self._type_civil = None
            return
        if self._type_point == "CIVIL":
            if value is not None and (not isinstance(value, str) or value.strip() == ""):
                raise ValueError("type_civil doit être une chaîne non vide.")
            self._type_civil = value
        else:
            raise ValueError("type_point doit être à CIVIL pour régler type_civil")
    
    
    # ------- taille_civil -------
    @property
    def taille_civil(self):
        return self._taille_civil
    
    @taille_civil.setter
    def taille_civil(self, value):
        if value is None:
            self._taille_civil = None
            return
        if self._type_point == "CIVIL":
            if not isinstance(value, str):
                raise ValueError("taille_civil doit être une chaine de caractères ('petit', 'moyen' ou 'grand')")
            elif value not in ["petit", "moyen", "grand"]:
                raise ValueError("taille_civil doit être 'petit', 'moyen' ou 'grand'.")
            else:
                self._taille_civil = value
        else:
            raise ValueError("type_point doit être à CIVIL pour régler taille_civil")
        

    # ------- acces_public -------
    @property
    def acces_public(self):
        return self._acces_public
    
    @acces_public.setter
    def acces_public(self, value):
        if value is None:
            self._acces_public = None
            return
        if self._type_point == "CIVIL":
            if value is not None and (not isinstance(value, str) or value.strip() == ""):
                raise ValueError("acces_public doit être une chaîne non vide.")
            self._acces_public = value
        else:
            raise ValueError("type_point doit être à CIVIL pour régler acces_public")    
    

    # ------- verifie_civil -------
    @property
    def verifie_civil(self):
        return self._verifie_civil
    
    @verifie_civil.setter
    def verifie_civil(self, value):
        if value is None:
            self._verifie_civil = None
            return
        if self._type_point == "CIVIL":
            if value is not None and not isinstance(value, bool):
                raise ValueError("verifie_civil doit être un boolean.")
            self._verifie_civil = value
        else:
            raise ValueError("type_point doit être à CIVIL pour régler verifie_civil") 
        
    

    @classmethod
    def from_dict(cls, data: dict):
        """Convertit un dictionnaire MongoDB en instance de WaterPoints"""
        if not data:
            return None
        
        # Créons une copie pour manipuler les données avant l'instanciation
        d = data.copy()
        
        # On s'assure que les dates sont traitées avant d'appeler le constructeur
        # Cela garantit que les setters recevront des objets manipulables
        for field in ["date_crea", "date_maj", "derniere_verification"]:
            if field in d and d[field] is not None:
                # Si c'est déjà un objet datetime on laisse tel quel
                # Sinon, le setter s'occupera de la conversion via _validate_date
                pass
        
        # On utilise le constructeur pour passer par les setters de validation
        return cls(
            id=data.get("_id"),
            location=data.get("location"),
            date_crea=data.get("date_crea"),
            date_maj=data.get("date_maj"),
            utilisateur=data.get("utilisateur"),
            carto_ref=data.get("carto_ref"),
            statut=data.get("statut"),
            press_debit=data.get("press_debit"),
            debit_1_bar=data.get("debit_1_bar"),
            numero_pei=data.get("numero_pei"),
            insee5=data.get("insee5"),
            type_nature=data.get("type_nature"),
            vol_eau_min=data.get("vol_eau_min"),
            accessibilite=data.get("accessibilite"),
            disponibilite=data.get("disponibilite"),
            derniere_verification=data.get("derniere_verification"),
            nb_raccordement=data.get("nb_raccordement"),
            type_point=data.get("type_point"),
            type_civil=data.get("type_civil"),
            taille_civil=data.get("taille_civil"),
            acces_public=data.get("acces_public"),
            verifie_civil=data.get("verifie_civil")
        )
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire simple pour FastAPI (JSON)"""
        # On récupère toutes les données
        data = {
            "id": str(self.id) if self.id else None,
            "location": self.location,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "date_crea": self.date_crea.isoformat() if self.date_crea else None,
            "date_maj": self.date_maj.isoformat() if self.date_maj else None,
            "utilisateur": self.utilisateur,
            "carto_ref": self.carto_ref,
            "statut": self.statut,
            "press_debit": self.press_debit,
            "debit_1_bar": self.debit_1_bar,
            "numero_pei": self.numero_pei,
            "insee5": self.insee5,
            "type_nature": self.type_nature,
            "vol_eau_min": self.vol_eau_min,
            "accessibilite": self.accessibilite,
            "disponibilite": self.disponibilite,
            "derniere_verification": self.derniere_verification.isoformat() if self.derniere_verification else None,
            "nb_raccordement": self.nb_raccordement,
            "type_point": self.type_point,
            "type_civil": self.type_civil,
            "taille_civil": self.taille_civil,
            "acces_public": self.acces_public,
            "verifie_civil": self.verifie_civil
        }
        return data
    