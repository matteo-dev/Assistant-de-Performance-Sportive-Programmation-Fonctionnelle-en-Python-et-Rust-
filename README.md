# 🏋️‍♂️ Functional Sport Performance Assistant

Assistant d'entraînement intelligent conçu pour analyser la progression de la force (1RM estimé via Epley), surveiller la fatigue nerveuse (*ACWR*) et piloter la trajectoire de prise de masse (lissage EWMA), le tout en appliquant les paradigmes stricts de la **programmation fonctionnelle**.

## 🚀 Piliers de l'Architecture Fonctionnelle

1. **Zéro Mutabilité :** L'historique des entraînements est figé en mémoire via l'utilisation de `@dataclass(frozen=True)` pour garantir l'absence d'effets de bord de type mutation en place.
2. **Fonctions 100% Pures :** Chaque calcul (tonnage, 1RM, ratios de charge) prend des entrées immuables et retourne de nouvelles sorties de manière strictement déterministe.
3. **Évaluation par Flux :** Bannissement total des boucles impératives (`for`/`while`) au profit d'opérateurs de flux de données (`map`, `filter`, `reduce`, `itertools.accumulate`).
4. **Mémoïsation et Performance :** Exploitation de la transparence référentielle pour sécuriser les caches de l'application (`@st.cache_data`).

---

## 🛠️ Installation et Utilisation

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/votre-nom-d-utilisateur/functional-programming-sport-assistant.git](https://github.com/votre-nom-d-utilisateur/functional-programming-sport-assistant.git)
   cd functional-programming-sport-assistant
2. **Installer les dépendances et lancer le frontend :**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
