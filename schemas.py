from pydantic import BaseModel
from typing import Optional


# Création d'un colis
# Le statut est optionnel : si non fourni, le backend applique
# automatiquement le statut par défaut "Reçu en Chine".
class ColisCreate(BaseModel):

    client: str
    telephone: str
    produit: str
    poids: str
    destination: str
    statut: Optional[str] = None



# Réponse renvoyée pour un colis (création, liste, suivi, modification)
class ColisResponse(BaseModel):

    id: int
    numero_suivi: str
    client: str
    telephone: str
    produit: str
    poids: str
    destination: str
    statut: str



# Modification du statut d'un colis (corps de la requête PUT)
class StatutUpdate(BaseModel):

    statut: str



# Statistiques admin
class AdminStats(BaseModel):

    total_colis: int
    en_transit: int
    arrive_cameroun: int
    livre: int



# Ajout historique
class HistoriqueCreate(BaseModel):

    numero_colis: str
    statut: str
    localisation: str
