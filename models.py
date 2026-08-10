from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Colis(Base):

    __tablename__ = "colis"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    numero_suivi = Column(
        String,
        unique=True,
        index=True
    )


    client = Column(String)

    telephone = Column(String)

    produit = Column(String)

    poids = Column(String)

    destination = Column(String)

    statut = Column(String)



class HistoriqueSuivi(Base):

    __tablename__ = "historique_suivi"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    numero_colis = Column(
        String,
        index=True
    )


    statut = Column(String)

    localisation = Column(String)

    date = Column(
        DateTime,
        default=datetime.now
    )