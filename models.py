from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


# ============================================================
# COLIS
# ============================================================

class Colis(Base):
    __tablename__ = "colis"

    id = Column(Integer, primary_key=True, index=True)
    numero_suivi = Column(String, unique=True, index=True, nullable=False)
    client = Column(String, nullable=False)
    telephone = Column(String)
    produit = Column(String)
    poids = Column(String)
    destination = Column(String)
    statut = Column(String, default="Reçu en Chine")


# ============================================================
# HISTORIQUE DU SUIVI
# ============================================================

class HistoriqueSuivi(Base):
    __tablename__ = "historique_suivi"

    id = Column(Integer, primary_key=True, index=True)
    numero_colis = Column(String, index=True, nullable=False)
    statut = Column(String)
    localisation = Column(String)
    date = Column(DateTime, default=datetime.now)