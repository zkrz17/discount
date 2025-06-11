from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    produits = pd.read_csv("promos_nike.csv", keep_default_na=False)
    produits["PrixNum"] = pd.to_numeric(produits["Prix"], errors="coerce")
    produits = produits.dropna(subset=["PrixNum"])

    recherche = request.args.get("q", "").lower()
    if recherche:
        produits = produits[produits["Nom"].str.lower().str.contains(recherche)]

    if request.args.get("tri") == "prix":
        produits = produits.sort_values(by="PrixNum")

    return render_template("index.html", produits=produits.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)