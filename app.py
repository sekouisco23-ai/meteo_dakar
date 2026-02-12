from flask import Flask, jsonify
import os
import psycopg2
import pandas as pd

app = Flask(__name__)

# Récupération de l'URL de la base depuis les variables d'environnement
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_data():
    """
    Récupère les données depuis PostgreSQL et retourne un DataFrame pandas.
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        df = pd.read_sql("SELECT * FROM meteo_dakar ORDER BY date", conn)
        conn.close()
        return df
    except Exception as e:
        print("Erreur connexion :", e)
        return None

@app.route("/", methods=["GET"])
def home():
    """
    Page d'accueil simple pour indiquer que l'API fonctionne.
    """
    return "Bienvenue sur l'API météo de Dakar ! Visitez /meteo pour les données."

@app.route("/meteo", methods=["GET"])
def meteo():
    """
    Route qui retourne toutes les données météo en JSON.
    """
    df = get_data()
    if df is not None:
        return jsonify(df.to_dict(orient="records"))
    else:
        return jsonify({"error": "Impossible de récupérer les données"}), 500

if __name__ == "__main__":
    # Port 10000 ou celui fourni par Render via PORT env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
