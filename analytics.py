# Fichier python d'analyse des données d'entraînement, en suivant les principes de la programmation fonctionnelle.


# Importation des modules nécessaires 
from itertools import accumulate # Pour effectuer des opérations cumulatives sur des itérables
from datetime import date, timedelta
from typing import Tuple
from functools import reduce # Pour effectuer des réductions sur des itérables
from src.models import WorkoutRecord, WorkoutHistory


# Fonction pure pour calculer le 1 Rep Max estimé via la formule d'Epley
def calculate_1rm_epley(weight: float, reps: int) -> float:

    # La formule d'Epley est : 1RM = poids * (1 + reps / 30)
    return weight * (1.0 + reps / 30.0) if reps > 1 else weight

# Fonction pure pour extraire la progression du 1RM pour le Squat
def extract_squat_progression(history: WorkoutHistory) -> Tuple[float, ...]:

    # 1. On isole les squats
    squat_records = filter(lambda r: r.exercise == "Squat", history)
    
    # 2. On transforme les records en 1RM
    rm_progression = map(lambda r: calculate_1rm_epley(r.weight_kg, r.reps), squat_records)
    
    # On retourne un Tuple pour maintenir l'immuabilité
    return tuple(rm_progression)

# Fonction pure pour calculer le tonnage total soulevé sur un historique donné
def calculate_total_volume(history: WorkoutHistory) -> float:

    # On ne modifie pas l'historique, on retourne une nouvelle valeur avec map
    volumes = map(lambda r: r.weight_kg * r.reps, history)

    # On utilise reduce pour sommer les volumes sans boucle for
    return reduce(lambda acc, current: acc + current, volumes, 0.0)

# Fonction pure pour calculer le volume total sur une période donnée
def get_volume_for_period(history: WorkoutHistory, start_date: date, end_date: date) -> float:

    # Utilisation de filter pour ne garder que les enregistrements dans la période souhaitée
    in_range = filter(lambda r: start_date <= r.date <= end_date, history)

    # On réutilise notre fonction pure précédente
    return calculate_total_volume(tuple(in_range))

# Fonction pure pour calculer l'ACWR (Acute:Chronic Workload Ratio) à une date donnée
def calculate_acwr(history: WorkoutHistory, current_date: date) -> float:

    # Définition des périodes pour le calcul de l'ACWR
    acute_start = current_date - timedelta(days=7)
    chronic_start = current_date - timedelta(days=28)
    
    # Récupération des volumes pour les périodes définies
    acute_vol = get_volume_for_period(history, acute_start, current_date)
    # Moyenne hebdomadaire sur 4 semaines
    chronic_vol = get_volume_for_period(history, chronic_start, current_date) / 4.0 
    
    # Résultat déterministe, zéro effet de bord
    return acute_vol / chronic_vol if chronic_vol > 0 else 0.0

# Fonction pour extraire la tendance du poids de corps au fil du temps
def extract_bodyweight_trend(history: WorkoutHistory) -> tuple[date, float]:

    # On utilise un dictionnaire pour ne garder que le dernier poids de corps enregistré par date
    unique_days = {r.date: r.bodyweight_kg for r in history}
    sorted_trend = sorted(unique_days.items(), key=lambda item: item[0])
    
    # On sépare en deux tuples (dates, poids) grâce à zip
    if not sorted_trend:
         return (), ()
    dates, weights = zip(*sorted_trend)
    return tuple(dates), tuple(weights)

# Fonction pure pour calculer le lissage exponentiel (EWMA) d'une série de poids
def calculate_ewma(weights: tuple[float, ...], alpha: float = 0.3) -> tuple[float, ...]:
    if not weights:
        return ()
    
    # Utilisation de accumulate pour calculer le lissage exponentiel sans boucle for
    ewma_seq = accumulate(
        weights,
        # La formule est EWMA_t = alpha * X_t + (1 - alpha) * EWMA_{t-1}
        lambda acc, current_weight: alpha * current_weight + (1 - alpha) * acc
    )
    return tuple(ewma_seq)

# Fonction pure pour projeter la date à laquelle un poids cible sera atteint
def project_target_date(dates: tuple[date, ...], weights: tuple[float, ...], target_kg: float = 70.0) -> date | None:
    if len(weights) < 2:
        return None
    
    # Calcul du gain total et du nombre de jours entre le premier et le dernier enregistrement
    total_gain = weights[-1] - weights[0]
    total_days = (dates[-1] - dates[0]).days
    
    # Gestion des cas aberrants (perte de poids ou division par zéro) sans effet de bord
    if total_days == 0 or total_gain <= 0:
        return None
    
    # Calcul du taux de gain moyen par jour et estimation du nombre de jours nécessaires pour atteindre le poids cible
    daily_rate = total_gain / total_days
    remaining_weight = target_kg - weights[-1]
    
    # Projection mathématique pure
    days_needed = int(remaining_weight / daily_rate)
    return dates[-1] + timedelta(days=days_needed)