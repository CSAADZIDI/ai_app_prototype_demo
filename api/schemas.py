from pydantic import BaseModel, Field, field_validator
from typing import Literal

class House(BaseModel):
    
    """
    Représente les caractéristiques d'un bien immobilier.

    Attributes:
        surface_bati (float): Surface bâtie du bien en mètres carrés.
        nombre_pieces (int): Nombre total de pièces du bien.
        type_local (Literal["appartement", "maison"]): Type de logement, uniquement 'appartement' ou 'maison'.
        surface_terrain (float): Surface du terrain en mètres carrés.
        nombre_lots (int): Nombre de lots dans la copropriété (ou 0 si maison individuelle).
    """
    surface_bati: float = Field(..., example=80.0)
    nombre_pieces: int = Field(..., example=4)
    type_local: Literal["appartement", "maison"] = Field(..., example="maison")
    surface_terrain: float = Field(..., example=150.0)
    nombre_lots: int = Field(..., example=1)

    @field_validator("type_local", mode="before")
    @classmethod
    def normalize_type_local(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class CityHouse(BaseModel):
    """
    Contient un bien immobilier et la ville cible pour la prédiction.

    Attributes:
        ville (str): Ville où se situe le bien ('lille' ou 'bordeaux').
        features (House): Caractéristiques du bien.
    """
    ville: Literal["lille", "bordeaux"] = Field(..., example="lille")
    features: House


class Prediction(BaseModel):
    """
    Représente le résultat de la prédiction.

    Attributes:
        prix_m2_estime (float): Prix estimé au m².
        ville_modele (str): Ville utilisée pour le modèle.
        model (str): Nom du modèle utilisé (ex. 'RandomForestRegressor').
    """
    prix_m2_estime: float = Field(..., example=3500.50)
    ville_modele: str = Field(..., example="Lille")
    model: str = Field(..., example="RandomForestRegressor")
