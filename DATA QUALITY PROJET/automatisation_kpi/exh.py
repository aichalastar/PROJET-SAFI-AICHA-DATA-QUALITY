import pandas as pd
import numpy as np

def calculer_exhaustivite():
    """
    Calcule l'exhaustivité en comparant les volumes de deux fichiers CSV
    """
    
    # Lecture des fichiers CSV
    print("Lecture des fichiers CSV...")
    
    try:
        # Chargement du fichier mensuel
        df_mensuel = pd.read_csv('trafic_data_monthly.csv')
        print(f" Fichier mensuel chargé: {len(df_mensuel)} lignes")
        
        # Chargement du fichier OTARI
        df_otari = pd.read_csv('trafic_otari.csv')
        print(f"Fichier OTARI chargé: {len(df_otari)} lignes")
        
    except FileNotFoundError as e:
        print(f" Erreur: Fichier non trouvé - {e}")
        return
    except Exception as e:
        print(f" Erreur lors du chargement: {e}")
        return
    
    # Calcul des sommes
    print("\n Calcul des sommes...")
    
    # Somme du fichier mensuel (colonne total_brouille)
    somme_mensuel = df_mensuel['total_brouille'].sum()
    lignes_mensuel = len(df_mensuel[df_mensuel['total_brouille'].notna()])
    
    # Somme du fichier OTARI (colonne volume)
    somme_otari = df_otari['volume'].sum()
    lignes_otari = len(df_otari[df_otari['volume'].notna()])
    
    # Calcul de la différence absolue
    difference = abs(somme_mensuel - somme_otari)
    
    # Calcul de l'exhaustivité
    exhaustivite = (min(somme_mensuel, somme_otari) / max(somme_mensuel, somme_otari)) * 100
    
    # Affichage des résultats
    print("\n" + "="*60)
    print(" RÉSULTATS DU CALCUL D'EXHAUSTIVITÉ")
    print("="*60)
    
    print(f"\n FICHIER MENSUEL:")
    print(f"   Somme total_brouille: {somme_mensuel:,.2f}")
    print(f"   Nombre de lignes: {lignes_mensuel}")
    
    print(f"\n FICHIER OTARI:")
    print(f"   Somme volume: {somme_otari:,.2f}")
    print(f"   Nombre de lignes: {lignes_otari}")
    
    print(f"\n DIFFÉRENCE ABSOLUE:")
    print(f"   |Mensuel - OTARI|: {difference:,.2f}")
    
    print(f"\n EXHAUSTIVITÉ:")
    print(f"   Taux de couverture: {exhaustivite:.4f}%")
    
    # Interprétation
    print(f"\n INTERPRÉTATION:")
    if exhaustivite >= 95:
        print("    Excellente exhaustivité - Données très cohérentes")
    elif exhaustivite >= 80:
        print("     Bonne exhaustivité - Quelques écarts acceptables")
    elif exhaustivite >= 60:
        print("    Exhaustivité moyenne - Vérification recommandée")
    else:
        print("    Faible exhaustivité - Écarts importants détectés")
    
    print("="*60)
    
    # Retour des résultats pour utilisation ultérieure
    return {
        'somme_mensuel': somme_mensuel,
        'somme_otari': somme_otari,
        'difference': difference,
        'exhaustivite': exhaustivite,
        'lignes_mensuel': lignes_mensuel,
        'lignes_otari': lignes_otari
    }

def analyser_par_periode():
    """
    Analyse détaillée par période pour identifier les écarts
    """
    try:
        df_mensuel = pd.read_csv('trafic_data_monthly.csv')
        df_otari = pd.read_csv('trafic_otari.csv')
        
        print("\n ANALYSE PAR PÉRIODE:")
        print("-" * 40)
        
        # Groupement par période pour le fichier mensuel
        mensuel_par_periode = df_mensuel.groupby('periode')['total_brouille'].sum().reset_index()
        
        # Groupement par période pour le fichier OTARI
        otari_par_periode = df_otari.groupby('periode')['volume'].sum().reset_index()
        
        # Fusion des données
        comparaison = pd.merge(mensuel_par_periode, otari_par_periode, 
                              on='periode', how='outer', suffixes=('_mensuel', '_otari'))
        
        # Remplacement des NaN par 0
        comparaison = comparaison.fillna(0)
        
        # Calcul des différences et exhaustivité par période
        comparaison['difference'] = abs(comparaison['total_brouille'] - comparaison['volume'])
        comparaison['exhaustivite'] = np.where(
            (comparaison['total_brouille'] == 0) | (comparaison['volume'] == 0),
            0,
            (np.minimum(comparaison['total_brouille'], comparaison['volume']) / 
             np.maximum(comparaison['total_brouille'], comparaison['volume'])) * 100
        )
        
        # Affichage période par période
        for _, row in comparaison.iterrows():
            print(f"\n Période {row['periode']}:")
            print(f"   Mensuel: {row['total_brouille']:,.2f}")
            print(f"   OTARI: {row['volume']:,.2f}")
            print(f"   Différence: {row['difference']:,.2f}")
            print(f"   Exhaustivité: {row['exhaustivite']:.2f}%")
        
    except Exception as e:
        print(f" Erreur lors de l'analyse par période: {e}")

# Fonction principale
def main():
    """
    Fonction principale qui lance tous les calculs
    """
    print(" DÉMARRAGE DU CALCULATEUR D'EXHAUSTIVITÉ")
    print("="*60)
    
    # Calcul principal
    resultats = calculer_exhaustivite()
    
    if resultats:
        # Analyse détaillée par période
        analyser_par_periode()
        
        # Sauvegarde des résultats (optionnel)
        sauvegarder_resultats(resultats)

def sauvegarder_resultats(resultats):
    """
    Sauvegarde les résultats dans un fichier
    """
    try:
        with open('resultats_exhaustivite.txt', 'w', encoding='utf-8') as f:
            f.write("RÉSULTATS EXHAUSTIVITÉ\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Somme Mensuel: {resultats['somme_mensuel']:,.2f}\n")
            f.write(f"Somme OTARI: {resultats['somme_otari']:,.2f}\n")
            f.write(f"Différence: {resultats['difference']:,.2f}\n")
            f.write(f"Exhaustivité: {resultats['exhaustivite']:.4f}%\n")
        
        print(f"\n Résultats sauvegardés dans 'resultats_exhaustivite.txt'")
        
    except Exception as e:
        print(f"  Impossible de sauvegarder: {e}")

# Exécution du script
if __name__ == "__main__":
    main()
