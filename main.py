from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import random
import os


app = FastAPI(
    title="Tyson Logistics API"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "https://tagomo-logistique-frontend-pkgy.vercel.app",
        "https://tagomo-logistique-frontend.vercel.app"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =========================
# DATABASE
# =========================

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "colis.db"
)


def connexion():

    return sqlite3.connect(DATABASE)



def init_db():

    conn = connexion()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colis(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        client TEXT NOT NULL,

        telephone TEXT,

        produit TEXT,

        poids TEXT,

        destination TEXT,

        statut TEXT,

        numero_suivi TEXT UNIQUE

    )
    """)


    conn.commit()
    conn.close()



init_db()



# =========================
# MODELES
# =========================

class ColisCreate(BaseModel):

    client:str
    telephone:str
    produit:str
    poids:str
    destination:str
    statut:str = "Reçu en Chine"



class StatutUpdate(BaseModel):

    statut:str



# =========================
# GENERATEUR CODE
# =========================

def generer_numero():

    return "TYC-" + str(
        random.randint(
            1000000000,
            9999999999
        )
    )



# =========================
# CREATION COLIS
# =========================

@app.post("/colis")
def ajouter_colis(colis:ColisCreate):

    conn = connexion()
    cursor = conn.cursor()


    numero = generer_numero()


    try:

        cursor.execute(
            """
            INSERT INTO colis
            (
            client,
            telephone,
            produit,
            poids,
            destination,
            statut,
            numero_suivi
            )

            VALUES (?,?,?,?,?,?,?)

            """,

            (
                colis.client,
                colis.telephone,
                colis.produit,
                colis.poids,
                colis.destination,
                colis.statut,
                numero
            )
        )


        conn.commit()


        id_colis = cursor.lastrowid


    except sqlite3.IntegrityError:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Erreur génération numéro colis"
        )


    conn.close()


    return {

        "id":id_colis,

        "client":colis.client,

        "telephone":colis.telephone,

        "produit":colis.produit,

        "poids":colis.poids,

        "destination":colis.destination,

        "statut":colis.statut,

        "numero_suivi":numero

    }



# =========================
# LISTE ADMIN
# =========================

@app.get("/colis")
def liste_colis():

    conn = connexion()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM colis ORDER BY id DESC"
    )


    rows = cursor.fetchall()

    conn.close()


    return [

        {
            "id":r[0],
            "client":r[1],
            "telephone":r[2],
            "produit":r[3],
            "poids":r[4],
            "destination":r[5],
            "statut":r[6],
            "numero_suivi":r[7]

        }

        for r in rows

    ]



# =========================
# SUIVI CLIENT
# =========================

@app.get("/suivi/{numero_suivi}")
def suivi(numero_suivi:str):

    conn = connexion()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT * FROM colis
        WHERE numero_suivi=?
        """,
        (numero_suivi,)
    )


    colis = cursor.fetchone()


    conn.close()



    if not colis:

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )



    return {

        "id":colis[0],
        "client":colis[1],
        "telephone":colis[2],
        "produit":colis[3],
        "poids":colis[4],
        "destination":colis[5],
        "statut":colis[6],
        "numero_suivi":colis[7]

    }




# =========================
# MODIFICATION STATUT
# =========================

@app.put("/colis/{id}")
def modifier_statut(id:int, data:StatutUpdate):

    conn = connexion()
    cursor = conn.cursor()



    cursor.execute(
        "SELECT id FROM colis WHERE id=?",
        (id,)
    )


    existe = cursor.fetchone()



    if not existe:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Colis introuvable"
        )



    cursor.execute(
        """
        UPDATE colis
        SET statut=?
        WHERE id=?
        """,

        (
            data.statut,
            id
        )
    )


    conn.commit()
    conn.close()



    return {

        "message":"Statut modifié",

        "id":id,

        "statut":data.statut

    }




# =========================
# SUPPRESSION
# =========================

@app.delete("/colis/{id}")
def supprimer_colis(id:int):

    conn = connexion()
    cursor = conn.cursor()


    cursor.execute(
        "DELETE FROM colis WHERE id=?",
        (id,)
    )


    conn.commit()
    conn.close()


    return {
        "message":"Colis supprimé"
    }




# =========================
# STATISTIQUES
# =========================

@app.get("/admin/stats")
def stats():

    conn = connexion()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM colis"
    )

    total = cursor.fetchone()[0]



    cursor.execute(
        "SELECT COUNT(*) FROM colis WHERE statut='En transit'"
    )

    transit = cursor.fetchone()[0]



    cursor.execute(
        "SELECT COUNT(*) FROM colis WHERE statut='Arrivé Cameroun'"
    )

    arrive = cursor.fetchone()[0]



    cursor.execute(
        "SELECT COUNT(*) FROM colis WHERE statut='Livré'"
    )

    livre = cursor.fetchone()[0]


    conn.close()



    return {

        "total":total,

        "transit":transit,

        "arrive":arrive,

        "livre":livre

    }