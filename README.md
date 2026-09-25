# 🏋️‍♂️ Functional Sport Performance Assistant

Assistant d'entraînement intelligent conçu pour analyser la progression de la force (1RM estimé via Epley), surveiller la fatigue nerveuse (*ACWR*) et piloter la trajectoire de prise de masse (lissage EWMA), le tout en appliquant les paradigmes stricts de la **programmation fonctionnelle**.

## 🚀 Piliers de l'Architecture Fonctionnelle

1. **Zéro Mutabilité :** L'historique des entraînements est figé en mémoire via l'utilisation de `@dataclass(frozen=True)` pour garantir l'absence d'effets de bord de type mutation en place.
2. **Fonctions 100% Pures :** Chaque calcul (tonnage, 1RM, ratios de charge) prend des entrées immuables et retourne de nouvelles sorties de manière strictement déterministe.
3. **Évaluation par Flux :** Bannissement total des boucles impératives (`for`/`while`) au profit d'opérateurs de flux de données (`map`, `filter`, `reduce`, `itertools.accumulate`).
4. **Mémoïsation et Performance :** Exploitation de la transparence référentielle pour sécuriser les caches de l'application (`@st.cache_data`).

## English Below

Smart training assistant designed to analyze strength progression (1RM estimated via Epley), monitor neural fatigue (ACWR), and manage bulking trajectories (EWMA smoothing), all while applying strict functional programming paradigms.

## 🚀 Pillars of Functional Architecture

1. **Zero Mutability:** Workout history is frozen in memory using @dataclass(frozen=True) to ensure the complete absence of in-place mutation side effects.
*2. **100% Pure Functions:** Every calculation (tonnage, 1RM, load ratios) takes immutable inputs and returns new outputs in a strictly deterministic manner.
3. **Stream Evaluation:** Total ban on imperative loops (for/while) in favor of data stream operators (map, filter, reduce, itertools.accumulate).
4. **Memoization and Performance:** Leveraging referential transparency to secure application caches (@st.cache_data).

---

## 🛠️ Installation et Utilisation

1. **Cloner le dépôt / Clone the reposit :**
   ```bash
   git clone [https://github.com/votre-nom-d-utilisateur/functional-programming-sport-assistant.git](https://github.com/votre-nom-d-utilisateur/functional-programming-sport-assistant.git)
   cd functional-programming-sport-assistant
2. **Installer les dépendances et lancer le frontend / Install requirements and run frontend :**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
