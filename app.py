import base64
import html
import re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Wishlist de mon 1/4 de siècle", page_icon="🎀", layout="wide", initial_sidebar_state="collapsed")

wishlist = [
    {"nom":"Veste Penny Lane","prix":120,"categorie":"Mode","description":"Ceci n'est qu'une inspiii !!!","image":"https://drive.google.com/file/d/1ov-IYB2S7cxmCU4F4TiNK1uN-p341T6y/view?usp=drive_link","lien":"https://www.asos.com/fr/topshop/topshop-veste-jacquard-a-bordure-en-faux-fur-multicolore/prd/211043984?affid=31234&_CjwKCAjwxeHWBhBPEiwAiqtQ-T11Hsi8r3UgcoV_at3Nk1JzHLWYsikonzELeQAX4J1cP3S6hxvyDRoC7YYQAvD_BwE&channelref=product+search&ppcadref=24047998521||&utm_source=google&utm_medium=cpc&utm_campaign=24047998521&utm_content=&utm_term=&gad_source=1&gad_campaignid=24048051594&gbraid=0AAAAADqFjODT7lpI2aTvSFhloMHTlfWku&gclid=CjwKCAjwxeHWBhBPEiwAiqtQ-T11Hsi8r3UgcoV_at3Nk1JzHLWYsikonzELeQAX4J1cP3S6hxvyDRoC7YYQAvD_BwE"},
    {"nom":"Veste Afghane","prix":70,"categorie":"Mode","description":"Ceci n'est qu'une inspi (bis) !!!!!","image":"https://drive.google.com/file/d/1_aGUFvep0KRj8pBOZCpQdToyg9lQOnWq/view?usp=drive_link","lien":"https://shop.mango.com/fr/fr/p/teen/fille-teen/manteaux-et-vestes/manteaux/manteau-effet-daim-avec-fourrure/37028285/09/00?utm_source=bcLQBVEDxlA%7C0&utm_medium=affiliate&utm_campaign=rakuteneu&ranMID=53120&ranEAID=bcLQBVEDxlA&ranSiteID=bcLQBVEDxlA-Z_wLSPYl2WV5F4cuOR5srg"},
    {"nom":"Massage","prix":70,"categorie":"Bien-être","description":"S'il te reste de la monnaie, je veux bien un petit massage rapide...","image":"https://drive.google.com/file/d/1kkN3OLN8efa1SD4AundW1qm21jDnBkvN/view?usp=drive_link","lien":"https://www.pantoufle-massage.fr/soins"},
    {"nom":"Sac à main pour ma rentrée","prix":220,"categorie":"Mode","description":"Je veux un tote bag de luxe, for my daily life at Balenciaga !!!","image":"https://drive.google.com/file/d/1YAmsU0_pJetvidCmonS6Ok4BrtkqBCT4/view?usp=drive_link","lien":"https://fr.vestiairecollective.com/"},
    {"nom":"Escarpins Bobbies","prix":100,"categorie":"Mode","description":"Pas ma pointure sur le site, mais elles existent sur Vinted","image":"https://drive.google.com/file/d/1_-WgDkVqeQXbUsQSuVFhGmp6hnnQwQe4/view?usp=drive_link","lien":"https://www.bobbies.com/fr/4000784035-paloma-milk.html"},
    {"nom":"Gilet Agnès b.","prix":75,"categorie":"Mode","description":"Facilement trouvable à 60-70 euros en seconde main","image":"https://drive.google.com/file/d/1O1g_Chkm8nN43OmOslyuOsD4TnwzZQxA/view?usp=drive_link","lien":"https://www.agnesb.com/fr-eu/femme/pret-a-porter/cardigans/cardigan-pression-en-molleton-de-coton/0267M434_000.html"},
    {"nom":"Veste en cuir","prix":150,"categorie":"Mode","description":"J'en veux, j'en veux, j'en veuuuuux (et pas de fripe !!!!)","image":"https://drive.google.com/file/d/1Suvh7ZVYaZtnk2oWu2VHBY8DPFGoRHy7/view?usp=drive_link","lien":"https://fr.pinterest.com/pin/998039967434724691/"},
    {"nom":"Bottes de tous les jours (à talons)","prix":250,"categorie":"Mode","description":"Mon coup de cœur.","image":"https://static.massimodutti.net/assets/public/ae3b/a0b8/659a4fd4bc78/31303e490c80/11015850800-o2/11015850800-o2.jpg?ts=1792424085210&f=auto&w=850","lien":"https://www.massimodutti.com/fr/botte-a-talon-compense-en-cuir-l11015850?cS=800"},
    {"nom":"Pyjama cute","prix":40,"categorie":"Mode","description":"Pour bien dormir la nuit (bzzzz)","image":"https://drive.google.com/file/d/1XHmZ2KWViPV_pZz-njhiP0izxzTSy0BS/view?usp=drive_link","lien":"https://www2.hm.com/fr_fr/productpage.1353701001.html"},
    {"nom":"Pantalon un peu loufoque","prix":45,"categorie":"Mode","description":"À rayures, en cuir, en velours ou en couleurs criardes...","image":"https://drive.google.com/file/d/15xaSVFisfcETjIw8j1D43gdOMv-Hovzb/view?usp=drive_link","lien":"https://fr.pinterest.com/pin/891079476289376121/"},
    {"nom":"Carte cadeau voyage/week-end","prix":200,"categorie":"Culture","description":"Pour me permettre de découvrir le monde","image":"https://drive.google.com/file/d/1mKvYkvcPx8uKGzn1ZNyfCXIWDfS7Wz5H/view?usp=drive_link","lien":"https://www.flightgift.com/fr/"},
    {"nom":"Lecture","prix":15,"categorie":"Culture","description":"Pour ma culture G.","image":"https://drive.google.com/file/d/1zLMjYs_UNMZOfVHQ-oUrdIeJfad4OkfL/view?usp=drive_link","lien":"https://www.goodreads.com/en/book/show/241392662-i-want-you-to-be-happy"},
    {"nom":"Trousse de maquillage + makeup pour le bureau","prix":50,"categorie":"Bien-être","description":"Petite trousse complète à avoir dans mon sac pour être cute tous les jours !!!","image":"https://drive.google.com/file/d/18vmfx2an4RTtJHK48h1ieQID4NU0rTF7/view?usp=drive_link","lien":"https://www.zalando.fr/mango-trousse-de-toilette-green-m9151f09h-m11.html?ssku=M9151F09H-M110ONE000&lang=en"},
    {"nom":"Lingerie","prix":30,"categorie":"Mode","description":"Pour être bien au chaud","image":"https://drive.google.com/file/d/1BSTW1MIOHhl4ReLnOVwUL9HqScfTaEI-/view?usp=drive_link","lien":"https://www2.hm.com/fr_fr/productpage.1258869020.html"},
    {"nom":"Spectacle","prix":30,"categorie":"Culture","description":"Pour nourrir mon esprit et mon âme","image":"https://drive.google.com/file/d/1apeIl3CjPvFoJe2aBriQypbjNaTgBgzv/view?usp=drive_link","lien":"https://www.billetreduc.com/"},
    {"nom":"Kodak jetable","prix":25,"categorie":"Technologie","description":"Pour immortaliser mes souvenirs et enjoliver mes dumps Insta !","image":"https://drive.google.com/file/d/1ZL96ItcdgmA4pKKdSnP43TafsLPLYwL6/view?usp=drive_link","lien":"https://www.amazon.fr/Appareil-Photo-Jetable-KODAK-FUNSAVER/dp/B00083CZCK"},
    {"nom":"TTMC (celui qu'on n'a pas à la maison)","prix":30,"categorie":"Culture","description":"Mon jeu préféré EVERRR !!!","image":"https://drive.google.com/file/d/1LfECu-8w4bi2iDixmggZYofr2yFuZHhf/view?usp=drive_link","lien":"https://www.fnac.com/Jeu-de-societe-TTMC-Tu-te-mets-combien/a13602807/w-4"},
    {"nom":"Sac à bandoulière pour tous les jours","prix":200,"categorie":"Mode","description":"Dans une couleur passe-partout pour tous les jours","image":"https://drive.google.com/file/d/1F1Ro7KHX1XbVJMVsLyXTdB8UzsyiziOF/view?usp=drive_link","lien":"https://www.vinted.fr/"},
    {"nom":"Accessoires","prix":30,"categorie":"Accessoires","description":"Bandeau, serre-tête noir, ceinture, foulard, bonnet coloré, etc.","image":"https://drive.google.com/file/d/1twn7WnzGvrMUdJt7EKfO5zNjyuD64rNq/view?usp=drive_link","lien":"https://www.zalando.fr/promo-femme/"},
    {"nom":"Pulls/Vestes 100% laine","prix":50,"categorie":"Mode","description":"Pour joindre l'utile à l'agréable :)","image":"https://drive.google.com/file/d/15rYKzDbbOrlG8XMwuOrIaeyidvPkWV3U/view?usp=drive_link","lien":"https://www.zara.com/fr/fr/femme-cardigans-pulls-l8322.html?v1=2419844"},
    {"nom":"Veste en daim intérieur fourrure","prix":200,"categorie":"Mode","description":"Pour me tenir au chaud l'hiver","image":"https://drive.google.com/file/d/13J6EDpATr4kzr9VUM-NUlXi0hT8QXKZN/view?usp=drive_link","lien":"https://www.leapt.fr/product-page/shearling-faux-fur-coat-2colors"},
    {"nom":"Soin couleur chez le coiffeur","prix":220,"categorie":"Bien-être","description":"Un changement capillaire, je veux passer au clair pour l'hiver","image":"https://drive.google.com/file/d/1M0E_hS8561P1ai1dC--SmRgge3iLyQGO/view?usp=drive_link","lien":"https://www.treatwell.fr/"},
    {"nom":"Sac de luxe","prix":230,"categorie":"Mode","description":"Si le budget le permet et si pépite il y a...","image":"https://drive.google.com/file/d/1sgmXYRZMYwIDMrWQJfvYVQ-8ltgglKcc/view?usp=drive_link","lien":"https://fr.vestiairecollective.com/"},
    {"nom":"Lunettes de luxe","prix":60,"categorie":"Accessoires","description":"Une jolie paire de luxe de seconde main pour orner mon petit nez","image":"https://drive.google.com/file/d/1e1bfpZygvbsVMINj6hVG8J2d1jhrkTDw/view?usp=drive_link","lien":"https://fr.vestiairecollective.com/accessoires-femme/lunettes/prada/lunettes-prada-en-plastique-multicolore-71987231.shtml"},
    {"nom":"Mocassins Gucci","prix":230,"categorie":"Mode","description":"Pourquoi pas des mocassins Gucci à mon tour ?","image":"https://drive.google.com/file/d/13a5GYxNp9esZCCDb3Wjsix-QdZQb32gk/view?usp=drive_link","lien":"https://fr.vestiairecollective.com/search/?q=mocassins+Gucci#gender=Femme%231"}
]

def nettoyer_url(texte):
    if not texte:
        return ""
    texte = html.unescape(str(texte)).strip()
    match = re.search(r'href=["\']([^"\']+)["\']', texte, re.I)
    if match:
        return match.group(1).strip()
    return re.sub(r"<[^>]+>", "", texte).strip()

def lien_image_direct(url):
    """Transforme un lien Google Drive '.../file/d/ID/view' en lien d'image affichable."""
    m = re.search(r"drive\.google\.com/file/d/([\w-]+)", url) or re.search(r"drive\.google\.com/.*[?&]id=([\w-]+)", url)
    return f"https://lh3.googleusercontent.com/d/{m.group(1)}" if m else url

for numero, voeu in enumerate(wishlist, start=1):
    voeu["id"] = numero
    voeu["image"] = lien_image_direct(nettoyer_url(voeu.get("image")))
    voeu["lien"] = nettoyer_url(voeu.get("lien"))

DOSSIER_IMAGES = Path(__file__).parent / "images"

@st.cache_data(show_spinner=False)
def image_src(numero, url_distante):
    """Image locale (images/01.jpg, 02.jpg...) si elle existe, sinon l'URL d'origine."""
    for ext, mime in (("jpg", "jpeg"), ("jpeg", "jpeg"), ("png", "png"), ("webp", "webp")):
        chemin = DOSSIER_IMAGES / f"{numero:02d}.{ext}"
        if chemin.exists():
            return f"data:image/{mime};base64," + base64.b64encode(chemin.read_bytes()).decode()
    return url_distante

if "page" not in st.session_state: st.session_state.page = "accueil"
if "filtre" not in st.session_state: st.session_state.filtre = "Tous"

def ouvrir(): st.session_state.page = "wishlist"
def retour(): st.session_state.page = "accueil"
def filtrer(valeur): st.session_state.filtre = valeur

st.markdown("""
<style>
:root{--pink:#ff49ad;--pink2:#ff8bcb;--black:#0b0b0b;--yellow:#ffe55c;--cream:#fff8ef;--tan:#c6803e}
.stApp{background-color:#ffb1d8;background-image:radial-gradient(ellipse at 20% 30%,rgba(0,0,0,.16) 0 5px,transparent 6px),radial-gradient(ellipse at 72% 18%,rgba(112,55,14,.26) 0 9px,transparent 10px),linear-gradient(135deg,#ff8dca,#ffd0e7 46%,#ff78bf);background-size:90px 90px,130px 130px,auto;color:var(--black)}
header[data-testid="stHeader"]{background:transparent} #MainMenu,footer{visibility:hidden}.block-container{max-width:1320px;padding-top:1.5rem;padding-bottom:4rem}
.hero{min-height:70vh;display:flex;align-items:center;justify-content:center;text-align:center}.hero-card{width:min(900px,95%);padding:4.3rem 2rem;border:5px solid #000;border-radius:42px;box-shadow:14px 14px 0 var(--pink),21px 21px 0 #000;background-color:#cd8847;background-image:radial-gradient(ellipse,#000 0 22%,#67340e 23% 39%,transparent 41%);background-size:70px 52px;transform:rotate(-1deg)}
.badge{display:inline-block;background:var(--yellow);border:3px solid #000;border-radius:999px;padding:.5rem 1.1rem;font-weight:950;letter-spacing:2px;box-shadow:5px 5px 0 #000}.hero h1,.title{font-family:"Brush Script MT","Segoe Script",cursive;color:var(--pink);-webkit-text-stroke:2px #000;text-shadow:4px 4px 0 #fff,8px 8px 0 #000}.hero h1{font-size:clamp(4rem,10vw,8.5rem);line-height:.82;margin:1.3rem 0}.tagline{display:inline-block;background:#fff;border:3px solid #000;border-radius:15px;padding:.8rem 1.2rem;font-weight:900;box-shadow:5px 5px 0 var(--pink)}
.title{text-align:center;font-size:clamp(4rem,8vw,7rem);line-height:1;margin:.4rem 0}.intro{width:fit-content;margin:1rem auto 2rem;background:var(--yellow);border:3px solid #000;border-radius:999px;padding:.6rem 1.1rem;font-weight:950;box-shadow:4px 4px 0 #000}
div[data-testid="stButton"]>button{min-height:50px;background:#fff;color:#000;border:3px solid #000;border-radius:999px;font-weight:950;box-shadow:5px 5px 0 #000;transition:.15s}div[data-testid="stButton"]>button:hover{background:var(--pink);color:#000;border-color:#000;transform:translate(3px,3px);box-shadow:2px 2px 0 #000}
.filter-label{text-align:center;font-weight:950;letter-spacing:2px;text-transform:uppercase;margin:1rem 0}.counter{width:fit-content;margin:1.6rem auto 2.2rem;background:#000;color:#fff;padding:.65rem 1.1rem;border-radius:999px;font-weight:900;box-shadow:5px 5px 0 var(--pink)}
.card{display:block;position:relative;height:430px;overflow:hidden;margin-bottom:2rem;border:4px solid #000;border-radius:26px;background:#fff;box-shadow:8px 8px 0 var(--pink),12px 12px 0 #000;text-decoration:none!important;transition:.2s}.card:hover{transform:translateY(-7px) rotate(-1deg);box-shadow:13px 13px 0 var(--yellow),17px 17px 0 #000}.card img{width:100%;height:100%;object-fit:cover;transition:.35s}.card:hover img{transform:scale(1.055);filter:saturate(1.12)}
.number,.price{position:absolute;top:14px;border:3px solid #000;font-weight:950;box-shadow:3px 3px 0 #000}.number{left:14px;width:43px;height:43px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:var(--yellow);transform:rotate(-8deg)}.price{right:14px;background:var(--pink);padding:.48rem .78rem;border-radius:999px;transform:rotate(3deg)}
.caption{position:absolute;left:13px;right:13px;bottom:13px;background:rgba(255,255,255,.95);border:3px solid #000;border-radius:16px;padding:.85rem 1rem;color:#000;font-weight:950;font-size:1.05rem;line-height:1.1;box-shadow:4px 4px 0 var(--pink)}.cat{display:block;color:#e90079;font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.2rem}.arrow{float:right;background:#000;color:#fff;border-radius:50%;width:27px;height:27px;text-align:center;line-height:27px}
.sep{height:7px;margin:3rem 0 2rem;border:2px solid #000;border-radius:999px;background:repeating-linear-gradient(90deg,#000 0 25px,var(--pink) 25px 50px,var(--yellow) 50px 75px)}
@media(max-width:640px){.block-container{padding-left:.8rem;padding-right:.8rem}.hero-card{padding:3.2rem 1rem;box-shadow:8px 8px 0 var(--pink),12px 12px 0 #000}.hero h1{font-size:clamp(3.5rem,18vw,5.5rem)}.card{height:480px}}
</style>
""", unsafe_allow_html=True)

if st.session_state.page == "accueil":
    st.markdown('''<div class="hero"><div class="hero-card"><span class="badge">BIRTHDAY EDITION • 25</span><h1>Wishlist de mon<br>1/4 de siècle</h1><div class="tagline">25 envies pour célébrer mes 25 ans ✦</div></div></div>''', unsafe_allow_html=True)
    a,b,c=st.columns([1.4,1,1.4])
    with b: st.button("OUVRIR MA WISHLIST 💋",on_click=ouvrir,use_container_width=True)
else:
    st.markdown('<h1 class="title">Mes 25 voeux (liste non-exhaustive)</h1><div class="intro">Clique sur une photo pour découvrir l’article ✦</div><div class="filter-label">Choisis ton niveau de générosité</div>',unsafe_allow_html=True)
    options=[("TOUT VOIR","Tous"),("MOINS DE 50 €","<50"),("50–100 €","50-100"),("100–150 €","100-150"),("PLUS DE 150 €",">150")]
    cols=st.columns(5,gap="small")
    for col,(label,value) in zip(cols,options):
        with col: st.button(("♥ " if st.session_state.filtre==value else "")+label,key="f"+value,on_click=filtrer,args=(value,),use_container_width=True)
    f=st.session_state.filtre
    if f=="<50": items=[v for v in wishlist if v["prix"]<50]
    elif f=="50-100": items=[v for v in wishlist if 50<=v["prix"]<=100]
    elif f=="100-150": items=[v for v in wishlist if 100<v["prix"]<=150]
    elif f==">150": items=[v for v in wishlist if v["prix"]>150]
    else: items=wishlist
    st.markdown(f'<div class="counter">{len(items)} ENVIE(S) SUR {len(wishlist)}</div>',unsafe_allow_html=True)
    for start in range(0,len(items),3):
        cols=st.columns(3,gap="large")
        for index,(col,v) in enumerate(zip(cols,items[start:start+3]),start=start+1):
            with col:
                name=html.escape(v["nom"],quote=True); cat=html.escape(v["categorie"],quote=True); image=html.escape(image_src(v["id"],v["image"]),quote=True); link=html.escape(v["lien"],quote=True)
                st.markdown(f'''<div class="card-box"><a class="card" href="{link}" target="_blank" rel="noopener noreferrer"><img src="{image}" alt="{name}" loading="lazy" referrerpolicy="no-referrer"><span class="number">{index:02d}</span><span class="price">{v["prix"]} €</span><span class="caption"><span class="cat">{cat}</span>{name}<span class="arrow">↗</span></span></a></div>''',unsafe_allow_html=True)
    st.markdown('<div class="sep"></div>',unsafe_allow_html=True)
    x,y=st.columns([1,3])
    with x: st.button("← RETOUR À L’ACCUEIL",on_click=retour,use_container_width=True)
