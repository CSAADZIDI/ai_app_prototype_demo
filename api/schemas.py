from pydantic import BaseModel, Field, field_validator
from typing import Literal

class House(BaseModel):
    """
    Représente les caractéristiques d'un bien immobilier.

    Attributes:
        surface_bati (float): Surface bâtie du bien en mètres carrés.
        nombre_pieces (int): Nombre total de pièces du bien.
        type_local (Literal["appartement", "maison"]): Type de logement.
        surface_terrain (float): Surface du terrain en mètres carrés.
        nombre_lots (int): Nombre de lots.
    """

    surface_bati: float = Field(
        ...,
        json_schema_extra={"example": 80.0}
    )
    nombre_pieces: int = Field(
        ...,
        json_schema_extra={"example": 4}
    )
    type_local: Literal["appartement", "maison"] = Field(
        ...,
        json_schema_extra={"example": "maison"}
    )
    surface_terrain: float = Field(
        ...,
        json_schema_extra={"example": 150.0}
    )
    nombre_lots: int = Field(
        ...,
        json_schema_extra={"example": 1}
    )

    @field_validator("type_local", mode="before")
    @classmethod
    def normalize_type_local(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class CityHouse(BaseModel):
    """
    Contient un bien immobilier et la ville cible pour la prédiction.
    """

    ville: Literal["lille", "bordeaux"] = Field(
        ...,
        json_schema_extra={"example": "lille"}
    )
    features: House


class Prediction(BaseModel):
    """
    Représente le résultat de la prédiction.
    """

    prix_m2_estime: float = Field(
        ...,
        json_schema_extra={"example": 3500.50}
    )
    ville_modele: str = Field(
        ...,
        json_schema_extra={"example": "Lille"}
    )
    model: str = Field(
        ...,
        json_schema_extra={"example": "RandomForestRegressor"}
    )
