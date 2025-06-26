import pandas as pd
from datetime import datetime, date
# import os

class AutomatisationRequetes:
    def __init__(self, annee=None, mois=None):
        # Utiliser la date actuelle si non spécifiée
        if annee is None or mois is None:
            today = date.today()
            self.annee = annee or today.year
            self.mois = mois or today.month
        else:
            self.annee = annee
            self.mois = mois
    
    def requete_parc_actif(self):
        """Génère la requête pour vérifier que la colonne segment marché est bien renseignée"""
        return f"""
-- PARC ACTIF - Vérification segment marché
SELECT concat(year, month) as periode, segment_marche, count(distinct msisdn) as parc
FROM monthly_clients
WHERE year = {self.annee} AND month = {self.mois} AND parc = 1
GROUP BY year, month, segment_marche
ORDER BY month;"""
    
    def requete_ca_recharge(self):
        """Génère la requête pour comparer les données de reporting CA monthly et celles de recharge detail in"""
        return f"""
-- CA RECHARGE - Comparaison reporting monthly vs recharge detail
SELECT year, month, formule_dmgp, segment_marche, segment_recharge,
    sum(ca_cartes) as cartes,
    sum(ca_credit_om) as credit,
    sum(ca_iah) as iah,
    sum(ca_pass_glob_om_jour) as pass1_glob_om,
    sum(ca_seddo) as seddo,
    sum(ca_recharges) as recharges,
    sum(ca_wave) as wave,
    sum(ca_ht) as ht,
    sum(nb_subs) as parc
FROM refined_vue360.reporting_ca_monthly
WHERE year = {self.annee} AND parc = 1
GROUP BY year, month, formule_dmgp, segment_marche, segment_recharge
ORDER BY month;

-- Requête complémentaire pour recharge detail
SELECT sum(montant)/1239 as ca_ht_year_month_canal_recharge
FROM refined_recharge.recharge_in_detail
WHERE year IN (LastYear) AND month IN (LastMonth) AND lower(canal_recharge)
IN ('ca wave', 'ca seddo', 'ca pass glob om jour', 'ca credit om', 'ca cartes', 'ca iah')
GROUP BY msisdn, year, month, canal_recharge;"""
    
    def requete_trafic_data(self):
        """Génère la requête pour comparer les données de reporting trafic data monthly et celles de dump otarie"""
        return f"""
-- TRAFIC DATA - Comparaison reporting monthly vs dump otarie
SELECT concat(year, month) as periode, year, month, segment_marche,
    sum(total_volume_go) as total,
    sum(trafic_4g_go) as traf_4G,
    sum(parc_4g) as parc_4g,
    sum(trafic_5g_go) as traf_5G,
    sum(parc_5g) as parc_5g
FROM refined_vue360.reporting_trafic_data_monthly
GROUP BY year, month, segment_marche;

-- Requête complémentaire pour dump otarie
SELECT concat(year, month) as periode, year, month, substr(msisdn, 4, 2) as debut_numero,
    sum(total_volume)/1000000000 as volume
FROM trusted_pfs.dump_otarie
WHERE year = {self.annee} AND month = {self.mois}
GROUP BY year, month, substr(msisdn, 4, 2);"""
    
    def generer_toutes_requetes(self):
        """Génère toutes les requêtes et les sauvegarde dans un fichier"""
        requetes = {
            "PARC_ACTIF": self.requete_parc_actif(),
            "CA_RECHARGE": self.requete_ca_recharge(),
            "TRAFIC_DATA": self.requete_trafic_data()
        }
        
        # Nom du fichier avec date
        nom_fichier = f"requetes_mensuelles_{self.annee}_{self.mois:02d}.sql"
        
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(f"-- REQUÊTES AUTOMATISÉES POUR {self.mois:02d}/{self.annee}\n")
            f.write(f"-- Générées le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for nom, requete in requetes.items():
                f.write(f"{requete}\n\n")
                f.write("-" * 80 + "\n\n")
        
        print(f" Requêtes sauvegardées dans: {nom_fichier}")
        return requetes

# ====
# UTILISATION
# ====

def main():
    print(" AUTOMATISATION DES REQUÊTES MENSUELLES")
    print("="*50)
    
    # Création de l'instance (utilise le mois/année actuel par défaut)
    # Ou spécifiez: AutomatisationRequetes(annee=2025, mois=6)
    auto = AutomatisationRequetes() 
    
    print(f" Période: {auto.mois:02d}/{auto.annee}")
    
    # Génération des requêtes
    print("\n Génération des requêtes...")
    requetes = auto.generer_toutes_requetes()
    
    print("\n Terminé!")

if __name__ == "__main__":
    main()

# Pour un mois spécifique:
# auto_juin = AutomatisationRequetes(annee=2025, mois=6)
# requetes_juin = auto_juin.generer_toutes_requetes()

 




