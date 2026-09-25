# Fichier python de tests unitaires pour les fonctions d'analyse de données d'entraînement.


# Importation des modules nécessaires pour les tests
import pytest # Framework de test pour Python
from datetime import date
from models import WorkoutRecord
from analytics import (
    calculate_1rm_epley,
    extract_squat_progression,
    calculate_total_volume,
    calculate_acwr,
    extract_bodyweight_trend,
    get_volume_for_period,
    calculate_ewma,
    project_target_date
)


# Utilisation de pytest.fixture pour fournir des données simulées aux tests
@pytest.fixture

# Fonction qui fournit un historique d'entraînement simulé pour les tests
def mock_history() -> tuple[WorkoutRecord, ...]:
    return (

        # Début du cycle : 67kg, tout va bien, RPE modéré
        WorkoutRecord(date(2026, 9, 1), "Squat", weight_kg=80.0, reps=5, rpe=7, bodyweight_kg=67.0),
        WorkoutRecord(date(2026, 9, 3), "Bench Press", weight_kg=60.0, reps=8, rpe=7, bodyweight_kg=67.2),
        
        # Prise de masse en cours : 68.5kg, ça monte bien
        WorkoutRecord(date(2026, 9, 8), "Squat", weight_kg=85.0, reps=5, rpe=8, bodyweight_kg=68.5),
        
        # Le blocage psychologique commence : 69.5kg de poids de corps.
        # La charge fait peur (90kg), le RPE est au max (10), les reps chutent.
        WorkoutRecord(date(2026, 9, 15), "Squat", weight_kg=90.0, reps=3, rpe=10, bodyweight_kg=69.5),
        WorkoutRecord(date(2026, 9, 22), "Squat", weight_kg=90.0, reps=2, rpe=10, bodyweight_kg=69.8),
    )

# Fonctions de test pour vérifier le comportement des fonctions d'analyse

# Test de la fonction calculate_1rm_epley pour s'assurer qu'elle calcule correctement le 1RM estimé.
def test_calculate_1rm_epley():

    result = calculate_1rm_epley(80.0, 5)
    assert result == pytest.approx(93.33, rel=1e-2)
    assert calculate_1rm_epley(100.0, 1) == 100.0

# Test de la fonction extract_squat_progression pour vérifier qu'elle extrait correctement la progression du 1RM pour le Squat.
def test_extract_squat_progression(mock_history):
    progression = extract_squat_progression(mock_history)
    
    # On attend 4 valeurs car il y a 4 entraînements de Squat dans l'historique
    assert len(progression) == 4
    
    # Vérification du premier 1RM (80kg x 5) et du dernier (90kg x 2)
    assert progression[0] == pytest.approx(93.33, rel=1e-2)
    assert progression[-1] == pytest.approx(96.0, rel=1e-2)

# Test de la fonction calculate_total_volume pour vérifier qu'elle calcule correctement le tonnage global soulevé.
def test_calculate_total_volume(mock_history):

    total_volume = calculate_total_volume(mock_history)
    assert total_volume == 1755.0
