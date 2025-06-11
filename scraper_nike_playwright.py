from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scraper_nike():
    def extraire_float(texte):
        try:
            return float(texte.replace("$", "").replace(",", ".").strip())
        except:
            return 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://www.nike.com/w/sale-3yaep", timeout=90000)
            page.wait_for_selector('[data-testid="product-card"]', timeout=15000)
            time.sleep(2)
        except Exception as e:
            print("❌ Erreur pendant le chargement :", e)
            browser.close()
            return

        produits = page.query_selector_all('[data-testid="product-card"]')
        data = []

        for produit in produits:
            image = produit.query_selector("img")
            nom = image.get_attribute("alt") if image else "Sans nom"
            image_url = image.get_attribute("src") if image else ""

            # Prend le 1er prix trouvé (réduit ou non)
            prix_el = produit.query_selector('[data-testid="product-price"]')
            prix = 0
            if prix_el:
                texte = prix_el.inner_text()
                prix = extraire_float(texte)

            lien_tag = produit.query_selector("a")
            lien = lien_tag.get_attribute("href") if lien_tag else ""
            if lien and "http" not in lien:
                lien = f"https://www.nike.com{lien}"

            data.append({
                "Nom": nom,
                "Prix": f"{prix:.2f}" if prix > 0 else "",
                "PrixNum": prix,
                "Image": image_url,
                "Lien": lien
            })

        browser.close()

        df = pd.DataFrame(data)
        df = df[df["Prix"] != ""]
        df = df.fillna("")
        df.to_csv("promos_nike.csv", index=False, encoding="utf-8-sig")
        print("✅ CSV généré avec une seule colonne Prix")

scraper_nike()
