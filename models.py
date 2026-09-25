# Fichier Python implémentant le modèle de données pour l'application Streamlit.


# Importation des modules nécessaires 
from dataclasses import dataclass # Pour créer des classes de données immuables
from datetime import date
from typing import Tuple # Les tuple servent à représenter des collections immuables et hétérogènes


# Création d'une classe de données immuable représentant un enregistrement d'entraînement
@dataclass(frozen=True) # Frozen=True rend la classe immuable
class WorkoutRecord:
    date: date
    exercise: str
    weight_kg: float
    reps: int
    rpe: int  
    bodyweight_kg: float

# Définition d'un type pour représenter l'historique des entraînements comme un tuple de WorkoutRecord
WorkoutHistory = Tuple[WorkoutRecord, ...]