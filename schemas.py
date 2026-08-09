from pydantic import BaseModel


# Création d'un colis
class ColisCreate(BaseModel):

    client: str
    telephone: str
    produit: str
    poids: str
    destination: str
    statut: str



# Ajout historique
class HistoriqueCreate(BaseModel):

    numero_colis: str
    statut: str
    localisation: str