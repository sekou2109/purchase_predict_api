import pandas as pd
import os
import requests
import json

# --- CONFIGURATION ---
# 1. Chemin vers tes données
path_kedro = "/home/cytech/IA/IG3-IA/kedro_mlops/purchase-predict"
csv_path = os.path.join(path_kedro, "data/03_primary/primary.csv")

# 2. Ton IP d'Ingress (Vérifiée d'après tes logs)
url_api = "http://34.117.227.57/predict"

def run_test():
    print(f"🚀 Lecture du dataset : {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"❌ Erreur : Le fichier {csv_path} est introuvable !")
        return

    # Chargement et nettoyage
    dataset = pd.read_csv(csv_path)
    
    # On retire les colonnes inutiles pour le modèle
    cols_to_drop = ["user_session", "user_id", "purchased"]
    dataset = dataset.drop(columns=[c for c in cols_to_drop if c in dataset.columns])
    
    # FIX : On remplace les NaN par 0 pour éviter l'erreur JSON compliance
    dataset = dataset.fillna(0)

    # On prépare 10 lignes aléatoires au format dictionnaire
    sample_data = dataset.sample(n=10).to_dict(orient="records")

    print(f"📡 Envoi de la requête à : {url_api}")

    try:
        # Envoi de la requête POST
        response = requests.post(url_api, json=sample_data, timeout=10)
        
        # Vérification du statut
        if response.status_code == 200:
            print("✅ SUCCÈS ! Ton cluster Kubernetes a répondu.")
            print("📊 Prédictions reçues :")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"⚠️ Le serveur a répondu avec une erreur {response.status_code}")
            print(f"Détails : {response.text}")

    except Exception as e:
        print(f"❌ Erreur de connexion au cluster : {e}")

if __name__ == "__main__":
    run_test()