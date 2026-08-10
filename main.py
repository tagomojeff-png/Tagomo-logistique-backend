from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal


# Création des tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Tyson Logistics API",
    version="1.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ton-site-vercel.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =========================
# DATABASE
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# =========================
# TEST API
# =========================

@app.get("/")
def accueil():

    return {
        "message": "Tyson Logistics API fonctionne 🚚"
    }



# =========================
# AJOUTER UN COLIS
# =========================

@app.post("/colis", response_model=schemas.ColisResponse)
def ajouter_colis(
    colis: schemas.ColisCreate,
    db: Session = Depends(get_db)
):

    nouveau_colis = models.Colis(

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
# LISTE COLIS
# =========================

@app.get("/colis")
def liste_colis(
    db: Session = Depends(get_db)
):

    colis = db.query(models.Colis).all()

    return colis



# =========================
# SUIVI COLIS
# =========================

@app.get("/suivi/{numero_suivi}")
def suivi_colis(
    numero_suivi: str,
    db: Session = Depends(get_db)
):

    colis = db.query(models.Colis).filter(
        models.Colis.numero_suivi == numero_suivi
    ).first()


    if not colis:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )


    return colis



# =========================
# MODIFIER STATUT
# =========================

@app.put("/colis/{numero_suivi}")
def modifier_statut(
    numero_suivi: str,
    statut: str,
    db: Session = Depends(get_db)
):

    colis = db.query(models.Colis).filter(
        models.Colis.numero_suivi == numero_suivi
    ).first()


    if not colis:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )


    colis.statut = statut

    db.commit()

    db.refresh(colis)


    return colis