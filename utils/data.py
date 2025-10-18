import pandas as pd
import geopandas as gpd
import streamlit as st
from collections import Counter
import unicodedata
import re


colonnes_rename = {
    "Horodateur": "horodateur",
    "Adresse e-mail": "email",
    "Quel âge avez vous ?": "age",
    "Quel est votre genre ?": "genre",
    "Votre situation actuelle ?": "situation",
    "Quel est votre département ? (réponse en chiffre)": "departement",
    "Depuis quand collectionnez vous / avez vous repris ?": "anciennete_collection",
    "Êtes vous professionnel dans Pokémon ? (société)": "professionnel",
    "Avez-vous joué à des jeux de la lignée principale ?": "jeux_principaux",
    "Avez-vous joué à ces catégories de jeux hors lignée principale ?": "jeux_hors_lignee",
    "Avez-vous regardé l'animé Pokémon ?": "anime",
    "Quel sont vos 5 Pokémon préférés ? (séparez par des \"-\", sans fautes d'orthographe si possible)": "pokemon_favoris",
    "Quelle est votre génération préférée ?": "gen_preferee",
    "Par quelle génération êtes vous arrivés dans Pokémon ?": "gen_arrivee",
    "Etes-vous entrés dans l'univers Pokémon en premier par :": "porte_entree",
    "Que collectionnez vous ?": "collection_type",
    "De quelle manière collectionnez vous vos cartes non-gradées ? (plusieurs réponses possibles)": "non_grade_collection",
    "Collectionnez vous du scellé ?": "scelle",
    "Que collectionnez vous en scellé ? ": "scelle_type",
    "Pour quelle raison collectionnez vous du scellé ? ": "raison_scelle",
    "Que pensez-vous de l'avenir du scellé ? (Recollé, Stocks, ...)": "avenir_scelle",
    "Avez-vous des cartes gradées en collection ?": "grade",
    "Chez quelle société de gradation gradez vous ?": "societe_gradation",
    "Pour quelle raison gradez vous vos cartes ?": "raison_gradation",
    "Que pensez-vous de l'avenir du gradé ? ": "avenir_grade",
    "Dans quelles langues collectionnez vous ?": "langues_collection",
    "Quels sont les blocs que vous appréciez ? (on parle de cartes et pas de génération)": "blocs_aimes",
    "Quels blocs collectionnez vous ?": "blocs_collectionnes",
    "Quel est votre bloc préféré ?": "bloc_prefere",
    "Quelle est votre série préférée du bloc Wizard ?": "serie_preferee_wizard",
    "Quelle est votre série préférée du bloc Ex ?": "serie_preferee_ex",
    "Quelle est votre série préférée du bloc Diamant et Perle ?": "serie_preferee_dp",
    "Quelle est votre série préférée du bloc Platine ?": "serie_preferee_platine",
    "Quelle est votre série préférée du bloc HGSS ?": "serie_preferee_hgss",
    "Quelle est votre série préférée du bloc Noir et Blanc ?": "serie_preferee_nb",
    "Quelle est votre série préférée du bloc XY ?": "serie_preferee_xy",
    "Quelle est votre série préférée du bloc Soleil & Lune ?": "serie_preferee_sl",
    "Quelle est votre série préférée du bloc Épée & Bouclier ?": "serie_preferee_eb",
    "Quelle est votre série préférée du bloc Écarlate et Violet ?": "serie_preferee_ev",
    "Quelle est votre carte préférée du TCG \n(format de réponse attendu si possible : Nom présent sur la carte- Série - Numéro de la carte)\n\nExemple : Noctali Vmax - Évolution Céleste - 215": "carte_preferee",
    "Quelle est votre rareté Vintage préférée ?": "rarete_vintage_preferee",
    "Quelle est votre rareté Semi-Vintage préférée ?": "rarete_semivintage_preferee",
    "Quelle est votre rareté Récente préférée ?": "rarete_recente_preferee",
    "Quel est votre budget mensuel moyen tout achat confondu (Scellé, Cartes, Ouverture, ...)": "budget_mensuel",
    "A quelle fréquence achetez vous des cartes/ items ?": "freq_achat",
    "Sur quelles plateformes achetez vous vos items/ cartes ?": "plateformes_achat",
    "Si vous utilisez des plateformes d'enchères, lesquelles ?": "plateformes_encheres",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Prix]": "avis_enchere_prix",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Ambiance générale]": "avis_enchere_ambiance",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Qualité des formats]": "avis_enchere_formats",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Qualité des produits]": "avis_enchere_produits",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Petits lives]": "avis_enchere_petitslives",
    "Quel est votre avis sur ces plateformes d'enchère de manière générale concernant : [Lives évènements]": "avis_enchere_eventlives",
    "Que pensez vous des boutiques de cartes à l'unité en terme de : [Prix]": "avis_boutique_prix",
    "Que pensez vous des boutiques de cartes à l'unité en terme de : [Confiance - Fiabilité]": "avis_boutique_fiabilite",
    "Que pensez vous des boutiques de cartes à l'unité en terme de : [Dispo des produits]": "avis_boutique_dispo",
    "Êtes vous investisseur dans Pokémon ?": "investisseur",
    "A combien estimez vous la valeur de vos investissements ?": "valeur_investissements",
    "Quel est votre avis sur l'investissement dans Pokémon ?": "avis_investissement",
    "Avez vous déjà réalisé des échanges ?": "echanges",
    "L'état des cartes a t il une importance pour vous ?": "importance_etat",
    "Quels réseaux sociaux utilisez vous pour discuter-partager votre collection ?": "reseaux_sociaux",
    "Combien ouvrez vous de boosters en moyenne par mois ?": "boosters_par_mois",
    "Quel est votre rapport à l'ouverture ?": "rapport_ouverture",
    "Vous êtes vous déjà rendu en convention TCG ? (Royaume, Gala, Pictasia, Belgium, ...)": "convention_tcg",
    "Comment jugez vous les éléments suivants : [Prix d'entrée]": "avis_convention_prix",
    "Comment jugez vous les éléments suivants : [Qualité des exposants]": "avis_convention_exposants",
    "Comment jugez vous les éléments suivants : [Importance de leur existence]": "avis_convention_importance",
    "Comment jugez vous les éléments suivants : [Disponibilité des produits]": "avis_convention_dispo",
    "Comment jugez vous les éléments suivants : [Tarifs sur place]": "avis_convention_tarifs",
    "Comment jugez vous les éléments suivants : [Qualité de l'organisation]": "avis_convention_orga",
    "Comment jugez vous les éléments suivants : [Sécurité sur place]": "avis_convention_securite",
    "Si vous souhaitez compléter ": "complement_libre",
    "Avez vous déjà subi une arnaque liée à Pokémon ?": "arnaque",
    "Quel type d'arnaque ?": "type_arnaque",
    "Si vous souhaitez préciser :": "arnaque_precisions",
    "Quel contenu Pokémon consommez vous sur Youtube ?": "contenu_youtube",
    "Et quel contenu préférez vous ?": "contenu_youtube_prefere",
    "Notez le YouTube France selon ces points : [Qualité]": "avis_youtube_qualite",
    "Notez le YouTube France selon ces points : [Diversité des créateurs]": "avis_youtube_diversite",
    "Notez le YouTube France selon ces points : [Redondance contenus]": "avis_youtube_redondance",
    "Notez le YouTube France selon ces points : [Votre lassitude]": "avis_youtube_lassitude",
    "Si vous souhaitez approfondir vos propos :": "youtube_precisions",
    "Sur quelle plateforme consommez vous le plus de vidéos Pokémon ?": "plateforme_video_preferee",
    "Quel format préférez vous ?": "format_video_prefere",
    "Aimeriez vous créer du contenu autour de cette passion ?": "envie_creation_contenu",
    "Si vous souhaitez ajouter quelque chose, faire des suggestions :": "suggestions_libres",
    "Quel est votre jeu préféré de la lignée principale ?": "jeu_prefere_principal",
    "Quelle est votre catégorie de jeux hors lignée principale préférée ?": "jeu_prefere_horslignee",
    "A quelle fréquence vous rendez-vous en boutique ?": "freq_boutique",
    "A combien estimez vous la valeur de votre  collection de scellé ?": "valeur_scelle",
    "Quelles sociétés de gradation appréciez vous ? Bonne image, qualité du travail, ...\n(La question qui concerne la société chez laquelle vous gradez arrive plus tard)": "societes_gradation_appreciees",
    "Si vous voulez donner un avis plus général sur ces plateformes :": "avis_plateformes_general",
    "Quelle est votre boutique préférée ? (si possible l'orthographe exacte de l'enseigne)": "boutique_preferee",
    "Sur quoi investissez vous ?": "investissements_type",
    "Payez vous un service pour avoir votre collection en sécurité ?": "service_securite",
    "Les réponses sont anonymes": "anonyme",
    "A quelle fréquence vous rendez-vous en boutique ? [Confiance - Fiabilité]": "freq_boutique_fiabilite",
    "A quelle fréquence vous rendez-vous en boutique ? [Dispo des produits]": "freq_boutique_dispo",
}

# ----- Chargement des données avec cache -----
@st.cache_data
def load_data(path="data/q7.csv"):
    df = pd.read_csv(path)
    df = df.rename(columns=colonnes_rename)
    return df

@st.cache_data
def load_geojson():
    url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    gdf = gpd.read_file(url)
    gdf = gdf.rename(columns={"code": "departement"})
    return gdf


@st.cache_data
def count_departements(df):
    dept_counts = df['departement'].value_counts().reset_index()
    dept_counts.columns = ['departement', 'count']
    return dept_counts

@st.cache_data
def count_multi_choice_column(df: pd.DataFrame, column: str, sep: str = ",") -> pd.Series:
    all_items = df[column].dropna().apply(lambda x: [item.strip() for item in x.split(sep)])
    counter = Counter([item for sublist in all_items for item in sublist])
    return pd.Series(counter).sort_values(ascending=False)

@st.cache_data
def clean_and_count_column(df, column, sep="-"):
    def normalize(word):
        # Supprime accents
        word = unicodedata.normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8')
        # Supprime guillemets
        word = word.replace('"', '')
        # Supprime tirets entourés d'espaces et espaces multiples
        word = re.sub(r'\s*-\s*', '', word)
        word = re.sub(r'\s+', ' ', word)
        # Minuscules et strip
        return word.strip().lower()
    
    all_items = df[column].dropna().apply(lambda x: [normalize(w) for w in x.split(sep)])
    
    counter = Counter([item for sublist in all_items for item in sublist])
    
    counts_df = pd.DataFrame({
        "word": list(counter.keys()),
        "count": list(counter.values())
    }).sort_values(by="count", ascending=False)
    
    return counts_df

@st.cache_data
def normalize_card_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    
    # 1. tout en minuscule
    name = name.lower().strip()

    # 2. enlever accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # 3. espaces multiples -> un seul
    name = re.sub(r'\s+', ' ', name)

    # 4. forcer espaces autour des tirets
    name = re.sub(r'\s*-\s*', ' - ', name)

    # 5. supprimer tout après le 2e tiret (inclus)
    parts = name.split(" - ")
    if len(parts) > 2:
        name = " - ".join(parts[:2])

    # 6. strip final + mettre chaque mot en majuscule
    name = name.strip().title()

    return name