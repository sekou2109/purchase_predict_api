import pandas as pd
import os
import requests

# 1. On charge les données avant encodage
path_kedro = "/home/cytech/IA/IG3-IA/kedro_mlops/purchase-predict"
dataset = pd.read_csv(os.path.join(path_kedro, "data/03_primary/primary.csv"))
dataset = dataset.drop(["user_session", "user_id", "purchased"], axis=1)

# 2. On envoie 10 lignes au hasard à notre API via une requête POST
response = requests.post(
    "http://127.0.0.1:5000/predict", 
    json=dataset.sample(n=10).to_json()
).json()

print("Prédictions reçues de l'API :", response)