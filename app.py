from flask import Flask, jsonify
import os
import psycopg2
import pandas as pd

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_data():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")

        df = pd.read_sql(
            "SELECT * FROM meteo_dakar ORDER BY date_observation",
            conn
        )

        conn.close()
        return df

    except Exception as e:
        print("Erreur connexion :", e)
        return None


@app.route("/", methods=["GET"])
def home():
    return "Bienvenue sur l'API météo de Dakar ! Visitez /meteo pour les données."


@app.route("/meteo", methods=["GET"])
def meteo():
    df = get_data()

    if df is not None:
        return jsonify(df.to_dict(orient="records"))
    else:
        return jsonify({"error": "Impossible de récupérer les données"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
