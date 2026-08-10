from pydantic import BaseModel


class ColisBase(BaseModel):

    client: str
    telephone: str
    produit: str
    poids: str
    destination: str
    statut: str = "Reçu en Chine"



class ColisCreate(ColisBase):
    pass



class ColisResponse(ColisBase):

    id: int
    numero_suivi: str


    class Config:
        from_attributes = True