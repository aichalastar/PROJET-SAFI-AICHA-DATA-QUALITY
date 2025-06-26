#  AUTOMATISATION_KPI

Ce projet permet d'automatiser la génération de requêtes SQL mensuelles et de vérifier l’exhaustivité des données issues des fichiers de reporting (`trafic_data_monthly.csv`) et des extractions techniques (`trafic_otari.csv`).

---

## ~ Structure du projet

AUTOMATISATION_KPI/
├── config/             ← Paramètres globaux ou mois à analyser
│ └── params.json       ← { "annee": 2025, "mois": 6, "parc": 1 }

├── queries/            ← Requêtes SQL brutes
│ ├── parc_actif.sql
│ ├── ca_recharge.sql
│ └── trafic_data.sql

├── scripts/                ← Code Python principal
│ ├── aut_req.py            ← Génère les requêtes SQL mensuelles
│ └── exh.py                ← Calcule l'exhaustivité à partir des fichiers CSV

├── outputs/                ← Fichiers générés automatiquement
│ ├── requetes_mensuelles_2025_06.sql
│ ├── resultats_exhaustivite.txt
│ └── graphiques/           ← (optionnel) Visualisations, KPI, courbes

├── data/                   ← Données d’entrée (fichiers à comparer)
│ ├── trafic_data_monthly.csv
│ └── trafic_otari.csv

├── calculateur d'exh  -> Un affichage dans le navigateur et un bouton de téléchargement du fichier resultats_exhaustivite.txt
¬ run_all.py              ← Script global qui exécute toute la chaîne
└── README.md             ← Ce fichier de documentation


---

##  Fonctionnement des scripts

### ~ `scripts/aut_req.py`

Contient la **classe `AutomatisationRequetes`**, qui :
- Génère 3 requêtes SQL :
  - Parc actif
  - CA recharge
  - Trafic data
- Sauvegarde ces requêtes dans un fichier `.sql` par mois (ex: `requetes_mensuelles_2025_06.sql`)

```python
auto = AutomatisationRequetes(annee=2025, mois=6)
auto.generer_toutes_requetes()

~ scripts/exh.py
Compare les volumes dans trafic_data_monthly.csv vs trafic_otari.csv

Calcule les sommes globales

Compare période par période

Produit un fichier resultats_exhaustivite.txt avec :

Totaux

Écart absolu

Taux d'exhaustivité (%)

Interprétation des résultats (faible, moyenne, bonne...)

 calculateur d'exhaustivite 
Un affichage clair dans le navigateur

Un bouton de téléchargement du fichier resultats_exhaustivite.txt