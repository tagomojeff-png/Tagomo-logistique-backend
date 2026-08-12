import random

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
    # L'app n'utilise aucun cookie de session (l'admin est protégé par un
    # mot de passe stocké côté client), donc pas besoin de restreindre
    # les origines ni d'activer allow_credentials : ça élimine tout risque
    # de mismatch d'origine (casse, sous-domaine, preview Vercel, etc.)
    # qui pouvait faire échouer les requêtes CORS sur certains navigateurs.
    allow_origins=["*"],
    allow_credentials=False,
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
# STATUT PAR DEFAUT
# =========================

STATUT_PAR_DEFAUT = "Reçu en Chine"



# =========================
# GENERATION NUMERO DE SUIVI
# =========================
# Format : TYC-XXXXXXXXXX (10 chiffres)
# On vérifie l'unicité en base avant de le retourner.

def generer_numero_suivi(db: Session) -> str:

    while True:

        chiffres = "".join(
            str(random.randint(0, 9)) for _ in range(10)
        )

        numero = f"TYC-{chiffres}"

        existant = db.query(models.Colis).filter(
            models.Colis.numero_suivi == numero
        ).first()

        if not existant:
            return numero



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

    numero = generer_numero_suivi(db)

    statut = colis.statut if colis.statut else STATUT_PAR_DEFAUT

    nouveau_colis = models.Colis(
        numero_suivi=numero,
        client=colis.client,
        telephone=colis.telephone,
        produit=colis.produit,
        poids=colis.poids,
        destination=colis.destination,
        statut=statut,
    )

    db.add(nouveau_colis)
    db.commit()
    db.refresh(nouveau_colis)

    return nouveau_colis



# =========================
# LISTE COLIS
# =========================

@app.get("/colis", response_model=list[schemas.ColisResponse])
def liste_colis(
    db: Session = Depends(get_db)
):

    return db.query(models.Colis).all()



# =========================
# SUIVI COLIS
# =========================

@app.get("/suivi/{numero_suivi}", response_model=schemas.ColisResponse)
def suivi_colis(
    numero_suivi: str,
    db: Session = Depends(get_db)
):

    numero_nettoye = numero_suivi.strip()

    colis = db.query(models.Colis).filter(
        models.Colis.numero_suivi == numero_nettoye
    ).first()

    if not colis:
        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )

    return colis



# =========================
# MODIFIER STATUT (par id)
# =========================

@app.put("/colis/{id}", response_model=schemas.ColisResponse)
def modifier_statut(
    id: int,
    donnees: schemas.StatutUpdate,
    db: Session = Depends(get_db)
):

    colis = db.query(models.Colis).filter(
        models.Colis.id == id
    ).first()


    if not colis:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )


    colis.statut = donnees.statut

    db.commit()
    db.refresh(colis)

    return colis



# =========================
# SUPPRIMER UN COLIS (par id)
# =========================

@app.delete("/colis/{id}")
def supprimer_colis(
    id: int,
    db: Session = Depends(get_db)
):

    colis = db.query(models.Colis).filter(
        models.Colis.id == id
    ).first()


    if not colis:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )


    db.delete(colis)

    db.commit()


    return {"message": "Colis supprimé avec succès"}



# =========================
# STATISTIQUES ADMIN
# =========================

@app.get("/admin/stats", response_model=schemas.AdminStats)
def stats_admin(
    db: Session = Depends(get_db)
):

    tous_les_colis = db.query(models.Colis).all()

    total_colis = len(tous_les_colis)

    en_transit = sum(
        1 for c in tous_les_colis if c.statut == "En transit"
    )

    arrive_cameroun = sum(
        1 for c in tous_les_colis if c.statut == "Arrivé Cameroun"
    )

    livre = sum(
        1 for c in tous_les_colis if c.statut == "Livré"
    )


    return {
        "total_colis": total_colis,
        "en_transit": en_transit,
        "arrive_cameroun": arrive_cameroun,
        "livre": livre,
    }