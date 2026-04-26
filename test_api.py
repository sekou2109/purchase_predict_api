import pandas as pd
import os
import requests

# 1. Le chemin vers tes données locales sur ton student-laptop
path_kedro = "/home/cytech/IA/IG3-IA/kedro_mlops/purchase-predict"
dataset = pd.read_csv(os.path.join(path_kedro, "data/03_primary/primary.csv"))
dataset = dataset.drop(["user_session", "user_id", "purchased"], axis=1)

# 2. L'envoi de la requête vers ton serveur Google Cloud
# ⚠️ REMPLACE L'IP CI-DESSOUS PAR L'IP EXTERNE DE TA VM "docker" ⚠️
url_api = "https://purchase-predict-api-179670955030.us-central1.run.app/predict" #

print(f"Envoi de la requête à {url_api}...")

response = requests.post(
    url_api, 
    json=dataset.sample(n=10).to_json()
).json() #

print("Prédictions reçues de l'API Docker :", response)