from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import random
import string

import models
import schemas

from database import engine, SessionLocal


# Création des tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Tyson Logistics API",
    version="1.0"
)


# Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



def generer_numero_suivi():

    return "TYC-" + ''.join(
        random.choices(
            string.digits,
            k=10
        )
    )



@app.get("/")
def accueil():

    return {
        "message": "Tyson Logistics API fonctionne 🚚"
    }



# =========================
# AJOUTER UN COLIS
# =========================

@app.post(
    "/colis",
    response_model=schemas.ColisResponse
)
def ajouter_colis(
    colis: schemas.ColisCreate,
    db: Session = Depends(get_db)
):

    numero = generer_numero_suivi()


    nouveau_colis = models.Colis(

        numero_suivi=numero,

        client=colis.client,

        telephone=colis.telephone,

        produit=colis.produit,

        poids=colis.poids,

        destination=colis.destination,

        statut=colis.statut

    )


    db.add(nouveau_colis)

    db.commit()

    db.refresh(nouveau_colis)


    return nouveau_colis





# =========================
# LISTE DES COLIS
# =========================

@app.get(
    "/colis",
    response_model=List[schemas.ColisResponse]
)
def liste_colis(
    db: Session = Depends(get_db)
):

    return db.query(models.Colis).all()





# =========================
# SUIVI COLIS
# =========================

@app.get(
    "/suivi/{numero_suivi}",
    response_model=schemas.ColisResponse
)
def suivre_colis(
    numero_suivi: str,
    db: Session = Depends(get_db)
):


    colis = db.query(models.Colis).filter(
        models.Colis.numero_suivi == numero_suivi
    ).first()



    if colis is None:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )


    return colis





# =========================
# SUPPRIMER UN COLIS
# =========================

@app.delete(
    "/colis/{numero_suivi}"
)
def supprimer_colis(
    numero_suivi: str,
    db: Session = Depends(get_db)
):


    colis = db.query(models.Colis).filter(
        models.Colis.numero_suivi == numero_suivi
    ).first()



    if colis is None:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )



    db.delete(colis)

    db.commit()



    return {
        "message": "Colis supprimé avec succès"
    }