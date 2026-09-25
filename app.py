# Fichier principal de l'application Streamlit pour l'analyse de la progression en squat et la gestion de la fatigue.


# Importation des modules nécessaires 
import streamlit as st # Framework pour créer des applications web interactives en Python
from datetime import date
from src.models import WorkoutRecord
from src.analytics import extract_squat_progression, calculate_total_volume, calculate_1rm_epley, calculate_acwr, extract_bodyweight_trend, calculate_ewma, project_target_date


# Utilisation de st.cache_data pour mettre en cache les données simulées afin d'éviter de les recalculer à chaque interaction 
@st.cache_data


# Fonction pour charger des données simulées d'entraînement
def load_mock_data() -> tuple[WorkoutRecord, ...]:
    return (
        WorkoutRecord(date(2026, 9, 1), "Squat", 80.0, 5, 7, 67.0),
        WorkoutRecord(date(2026, 9, 8), "Squat", 85.0, 5, 8, 68.5),
        WorkoutRecord(date(2026, 9, 15), "Squat", 90.0, 3, 10, 69.5),
        WorkoutRecord(date(2026, 9, 22), "Squat", 90.0, 2, 10, 69.8),
        WorkoutRecord(date(2026, 9, 29), "Squat", 92.5, 3, 9, 70.1),
    )

# Fonction main de l'application Streamlit
def main():
    st.title("🏋️‍♂️ Assistant Data-Sportif & Biomécanique")
    st.write("Architecture 100% Fonctionnelle - Zéro Mutabilité")
    
    history = load_mock_data()
    
    # Création des onglets Streamlit
    tab1, tab2, tab3 = st.tabs(["📊 Progression & 1RM", "🧠 Fatigue & ACWR", "⚖️ Poids de corps (67 -> 70kg)"])
    
    with tab1:
        st.header("Analyse de la Force (Squat)")
        total_volume = calculate_total_volume(history)
        squat_1rm_progression = extract_squat_progression(history)
        dates = tuple(map(lambda r: r.date, filter(lambda r: r.exercise == "Squat", history)))
        
        st.metric(label="Volume Global Historique", value=f"{total_volume} kg")
        st.line_chart({"Date": dates, "1RM Estimé (kg)": squat_1rm_progression}, x="Date", y="1RM Estimé (kg)")
        
    with tab2:
        st.header("Gestion de la Fatigue & Système Nerveux")
        st.write("Le ratio ACWR optimal se situe entre 0.8 et 1.3. Au-delà, le risque de blessure et de blocage nerveux augmente (le fameux 'mur').")
        
        # On calcule l'ACWR à la date du dernier entraînement
        last_workout_date = history[-1].date
        acwr_score = calculate_acwr(history, last_workout_date)
        
        st.metric(label="ACWR Actuel", value=f"{round(acwr_score, 2)}")
        if acwr_score > 1.3:
            st.warning("⚠️ Attention : Surcharge aiguë détectée. Le blocage mental au squat vient probablement d'une fatigue du système nerveux central. Réduisez le volume.")
        else:
            st.success("✅ Charge d'entraînement optimale.")
            
    with tab3:
        st.header("⚖️ Trajectoire de Prise de Masse (EWMA)")
        st.write("Objectif : Atteindre les 70kg de manière contrôlée, filtré par lissage exponentiel (EWMA, α=0.3).")
        
        # 1. Extraction pure des données brutes
        dates_bw, weights = extract_bodyweight_trend(history)
        
        # 2. Application du modèle mathématique (Pipeline de données)
        ewma_weights = calculate_ewma(weights, alpha=0.3)
        target_date = project_target_date(dates_bw, ewma_weights, target_kg=70.0)
        
        # 3. Affichage des KPIs
        current_weight = weights[-1]
        st.metric(
            label="Poids Actuel vs Objectif (70kg)", 
            value=f"{current_weight} kg", 
            delta=f"{round(70.0 - current_weight, 1)} kg restants",
            delta_color="off"
        )
        
        if target_date:
            st.success(f"📈 Projection mathématique : Objectif des 70kg estimé au **{target_date.strftime('%d %B %Y')}**.")
        
        # 4. Graphique comparatif (Brut vs Lissé)
        import pandas as pd
        # Nous utilisons pandas temporairement juste pour le formatage attendu par Streamlit (st.line_chart)
        chart_data = pd.DataFrame({
            "Date": dates_bw,
            "Poids Brut (kg)": weights,
            "Tendance EWMA (kg)": ewma_weights
        }).set_index("Date")
        
        st.line_chart(chart_data)
if __name__ == "__main__":
    main()