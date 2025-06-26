from scripts.aut_req import AutomatisationRequetes
from scripts.exh import main as verifier_exhaustivite

def main():
    print("=== LANCEMENT DU PIPELINE KPI ===")
    
    # Étape 1 : Générer les requêtes SQL
    auto = AutomatisationRequetes(annee=2025, mois=6)
    auto.generer_toutes_requetes()
    
    # Étape 2 : Vérifier l'exhaustivité
    verifier_exhaustivite()
    
    print("\n✅ Pipeline terminé avec succès.")

if __name__ == "__main__":
    main()

