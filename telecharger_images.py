"""Télécharge toutes les images de la wishlist dans le dossier images/ (01.jpg, 02.jpg...).

Utilisation (dans le dossier de app.py) :
    python telecharger_images.py            # télécharge celles qui manquent
    python telecharger_images.py --force    # retélécharge tout
"""
import ast
import html
import io
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image  # déjà installé avec Streamlit

RACINE = Path(__file__).parent
DOSSIER = RACINE / "images"
DOSSIER.mkdir(exist_ok=True)
FORCE = "--force" in sys.argv
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def nettoyer_url(texte):
    if not texte:
        return ""
    texte = html.unescape(str(texte)).strip()
    m = re.search(r'href=["\']([^"\']+)["\']', texte, re.I)
    if m:
        return m.group(1).strip()
    return re.sub(r"<[^>]+>", "", texte).strip()


def charger_wishlist():
    arbre = ast.parse((RACINE / "app.py").read_text(encoding="utf-8"))
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign) and any(getattr(t, "id", "") == "wishlist" for t in noeud.targets):
            return ast.literal_eval(noeud.value)
    sys.exit("Liste 'wishlist' introuvable dans app.py")


def origine(url):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}/" if p.scheme and p.netloc else None


def candidats(url):
    """Liste des adresses à essayer (pour Google Drive : deux formes différentes)."""
    m = re.search(r"drive\.google\.com/file/d/([\w-]+)", url) or re.search(r"drive\.google\.com/.*[?&]id=([\w-]+)", url)
    if m:
        ident = m.group(1)
        return [f"https://lh3.googleusercontent.com/d/{ident}",
                f"https://drive.google.com/uc?export=download&id={ident}"]
    return [url]


def telecharger(url, lien):
    """Essaie plusieurs adresses et plusieurs 'referer' ; renvoie une image valide ou l'erreur."""
    erreur = "inconnue"
    for adresse in candidats(url):
        for referer in (origine(lien), origine(adresse), None):
            entetes = {"User-Agent": UA, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"}
            if referer:
                entetes["Referer"] = referer
            try:
                with urllib.request.urlopen(urllib.request.Request(adresse, headers=entetes), timeout=25) as r:
                    donnees = r.read()
                img = Image.open(io.BytesIO(donnees))
                img.load()  # vérifie que c'est bien une image (et pas une page HTML d'erreur)
                return img, None
            except Exception as e:  # noqa: BLE001
                erreur = str(e)
        # Drive : inutile d'insister avec d'autres 'referer' si le fichier est privé
    return None, erreur


def enregistrer(img, chemin_sans_ext):
    """Redimensionne (max 800 px de large) et convertit en JPEG léger."""
    img = img.convert("RGB")
    img.thumbnail((800, 1100))
    img.save(chemin_sans_ext.with_suffix(".jpg"), "JPEG", quality=82, optimize=True)


def main():
    wishlist = charger_wishlist()
    echecs = []
    for numero, v in enumerate(wishlist, start=1):
        nom = v.get("nom", "?")
        if not FORCE and any((DOSSIER / f"{numero:02d}.{e}").exists() for e in ("jpg", "jpeg", "png", "webp")):
            print(f"[deja la] {numero:02d} {nom}")
            continue
        url, lien = nettoyer_url(v.get("image")), nettoyer_url(v.get("lien"))
        image, erreur = telecharger(url, lien)
        if image is None:
            print(f"[ECHEC]   {numero:02d} {nom} -> {erreur}")
            echecs.append((numero, nom, url))
            continue
        try:
            enregistrer(image, DOSSIER / f"{numero:02d}")
            print(f"[OK]      {numero:02d} {nom}")
        except Exception as e:  # noqa: BLE001
            print(f"[ECHEC]   {numero:02d} {nom} -> format illisible ({e})")
            echecs.append((numero, nom, url))

    print()
    if echecs:
        print(f"{len(echecs)} image(s) à récupérer à la main. Enregistre-les dans images/ sous ce nom (jpg, png ou webp) :")
        for numero, nom, url in echecs:
            print(f"  images/{numero:02d}.jpg   <- {nom}\n      {url}")
    else:
        print("Toutes les images sont téléchargées. Relance l'app : streamlit run app.py")


if __name__ == "__main__":
    main()
