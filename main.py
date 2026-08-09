from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, SessionLocal


app = FastAPI(
    title="Tyson & Co Logistics"
)


# =====================
# DATABASE MODEL
# =====================

class Colis(Base):

    __tablename__ = "colis"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    numero = Column(
        String,
        unique=True,
        index=True
    )


    client = Column(String)

    telephone = Column(String)

    produit = Column(String)

    poids = Column(String)

    destination = Column(String)


    statut = Column(
        String,
        default="Reçu en Chine"
    )


    date_creation = Column(
        String,
        default=lambda:
        datetime.now().strftime("%d/%m/%Y")
    )


    historique = Column(
        String,
        default="Reçu en Chine"
    )




Base.metadata.create_all(bind=engine)



# =====================
# CORS
# =====================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)





def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()






# =====================
# TEST
# =====================

@app.get("/")
def home():

    return {

        "message":
        "Tyson & Co Logistics API active"

    }







# =====================
# GENERATE NUMBER
# =====================

def generer_numero(db):

    date = datetime.now().strftime("%Y%m%d")

    nombre = db.query(Colis).count()+1


    return f"TYC-{date}-{nombre:03d}"







# =====================
# AJOUT COLIS
# =====================

@app.post("/colis")
def ajouter_colis(

    data:dict,

    db:Session=Depends(get_db)

):


    colis = Colis(

        numero=generer_numero(db),

        client=data["client"],

        telephone=data["telephone"],

        produit=data["produit"],

        poids=data["poids"],

        destination=data["destination"],

        statut=data["statut"],

        historique=data["statut"]

    )


    db.add(colis)

    db.commit()

    db.refresh(colis)


    return colis







# =====================
# LISTE ADMIN
# =====================

@app.get("/colis")
def liste_colis(

    db:Session=Depends(get_db)

):

    return db.query(Colis).all()








# =====================
# SUIVI
# =====================

@app.get("/colis/{numero}")
def suivre_colis(

    numero:str,

    db:Session=Depends(get_db)

):


    colis = db.query(Colis).filter(

        Colis.numero == numero

    ).first()



    if not colis:

        return {

            "message":
            "Colis introuvable"

        }




    return colis







# =====================
# SUPPRIMER
# =====================

@app.delete("/colis/{id}")
def supprimer_colis(

    id:int,

    db:Session=Depends(get_db)

):


    colis = db.query(Colis).filter(

        Colis.id == id

    ).first()



    if colis:

        db.delete(colis)

        db.commit()



    return {

        "message":
        "Supprimé"

    }






# =====================
# CHANGER STATUT
# =====================

@app.put("/colis/{id}")
def modifier_statut(

    id:int,

    data:dict,

    db:Session=Depends(get_db)

):


    colis=db.query(Colis).filter(

        Colis.id==id

    ).first()



    if colis:


        colis.statut=data["statut"]


        colis.historique += (
            " → "
            + data["statut"]
        )


        db.commit()

        db.refresh(colis)



    return colis






# =====================
# STATS
# =====================

@app.get("/admin/stats")
def stats(

    db:Session=Depends(get_db)

):

    return {

        "total":
        db.query(Colis).count(),


        "transit":
        db.query(Colis)
        .filter(
            Colis.statut=="En transit"
        )
        .count(),


        "arrive":
        db.query(Colis)
        .filter(
            Colis.statut=="Arrivé Cameroun"
        )
        .count(),


        "livre":
        db.query(Colis)
        .filter(
            Colis.statut=="Livré"
        )
        .count()

    }