import streamlit as st
from utils.data import load_data, clean_and_count_column
from utils.viz import generic_multi_bar, generic_bar, generic_pie, generic_multi_pie, wordcloud_plot, sidebar_logo
import plotly.express as px
import pandas as pd
import numpy as np

sidebar_logo()
 
# st.plotly_chart(generic_pie(df, "serie_preferee_wizard"), use_container_width=True)
# st.plotly_chart(generic_multi_bar(df, "jeux_principaux", sep=",", horizontal=True, top_n=10), use_container_width=True)
# st.plotly_chart(generic_bar(df, "anciennete_collection", title="Bar anciennete_collection"), use_container_width=True)
# st.plotly_chart(generic_multi_pie(df, "ta_colonne", sep=",", protected_groups=["Du récent (EV, EB)","Du semi-vintage (SL, XY, NB)"]))

st.set_page_config(page_title="Les analyses", page_icon="🔍", layout="wide")


st.title("Comment consommez vous Pokémon ?")
st.markdown(
    """
    <div style="font-size:20px;">
        Cinquième partie - Dans cette section nous allons faire en sorte de faire parler ce qui se cache derrière les chiffres, faire des analyses plus poussées sur notre hobby préféré !
    </div>
    """,
    unsafe_allow_html=True
)
df = load_data()



st.markdown("---")  

st.markdown(
    """
    <div style="font-size:20px;">
        <b>Une histoire de générations ...</b>
    </div>
    """,
    unsafe_allow_html=True
)


# --- ANALYSE 1 : Génération d’arrivée vs Génération préférée ---

# Matrice de correspondance
matrix = pd.crosstab(df["gen_arrivee"], df["gen_preferee"])

# Scores
attraction_scores = (
    matrix.sum(axis=0) / matrix.sum(axis=1).reindex(matrix.columns, fill_value=0).replace(0, np.nan)
).fillna(0)

fidelite_scores = (
    pd.Series(np.diag(matrix), index=matrix.index) / matrix.sum(axis=1)
).fillna(0)

# DataFrames
attraction_df = attraction_scores.reset_index()
attraction_df.columns = ["Generation", "Attraction_Score"]

fidelite_df = fidelite_scores.reset_index()
fidelite_df.columns = ["Generation", "Fidelite_Score"]

# Heatmap
heatmap_fig = px.imshow(
    matrix,
    text_auto=True,
    color_continuous_scale="Viridis",
    labels=dict(x="Génération préférée", y="Génération d’arrivée", color="Nombre"),
    title="Correspondance entre génération d’arrivée et génération préférée"
)
heatmap_fig.update_layout(title_font_size=22)

# Barplot attraction
bar_fig = px.bar(
    attraction_df,
    x="Generation",
    y="Attraction_Score",
    text=attraction_df["Attraction_Score"].round(2),
    title="Score d’attraction des générations",
    labels={"Generation": "Génération", "Attraction_Score": "Score d’attraction"},
)
bar_fig.update_traces(textposition="outside")
bar_fig.update_layout(title_font_size=22, yaxis=dict(range=[0, attraction_df["Attraction_Score"].max() + 0.2]))

# --- Streamlit layout ---
col1, col2, col3 = st.columns([1.3, 1, 1])

with col1:
    st.plotly_chart(heatmap_fig, use_container_width=True)

with col2:
    st.plotly_chart(bar_fig, use_container_width=True)

with col3:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Cette heatmap montre les liens entre la génération <b>d’arrivée</b> et la <b>préférée</b>.<br><br>
        Le <b>score d’attraction</b> (graphique de droite) indique à quel point chaque génération attire des fans 
        d’autres époques :<br><br>
        • Un score &gt; 1 = génération très attractive, qui séduit au-delà de ses arrivants.<br>
        • Un score &lt; 1 = génération moins fédératrice.<br><br>
        Le <b>score de fidélité</b> (interne) mesure la proportion de fans restés attachés à leur génération d’origine.<br><br>
        Ces deux mesures permettent d’identifier les générations “fidèles” et celles “séductrices”.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)


# --- ANALYSE AUTOMATIQUE TEXTE ---

commentaire = """
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    La <b>2G ressort comme la plus attractive</b>, avec un score de 2.38, ce qui indique qu’elle attire beaucoup de fans venus d’autres générations.<br>
    À l’inverse, la 1G à ma (notre?) grande surprise est celle qui a perdu le plus de personnes au détriment d'autres générations !<br><br>
    Enfin, <b>la 9G est la plus fidèle</b>, conservant la plus grande part de ses arrivants d’origine, 100% !!! (Les hommes mentent, pas les chiffres !).<br>
    L'échantillon étant très faible c'est logique, <b>le vrai gagnant est la 4G avec 88.5%</b>, devant la 3G avec 75%.
</div>
"""
st.markdown(commentaire, unsafe_allow_html=True)






st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        <b>Situation professionnelle et argent ...</b>
    </div>
    """,
    unsafe_allow_html=True
)


# Introduction explicative
st.markdown(
    """
    <div style="font-size:20px;">
        Cette section vise à explorer la relation entre la situation professionnelle des collectionneurs (étudiant, salarié, freelance, etc.) et 
        leur budget mensuel dédié à la collection. 
    </div>
    """,
    unsafe_allow_html=True
)

# --- Vérification du nom de la colonne situation ---
if "situation" in df.columns:
    col_situation = "situation"
elif "situation_pro" in df.columns:
    col_situation = "situation_pro"
elif "situation_profe" in df.columns:  # fallback si nécessaire
    col_situation = "situation_profe"
else:
    st.error("Colonne 'situation' ou 'situation_pro' introuvable dans le DataFrame.")
    st.stop()

# --- Tranches fournies par toi (ordre logique) ---
ordre_tranches_display = [
    "-50€",        # j'interprète comme "<50€"
    "50- 100€",
    "100- 200€",
    "200- 300€",
    "300- 400€",
    "400- 700€",
    "700- 1000€",
    "+ de 1000€"
]

# --- Normalisation des valeurs pour faire correspondre proprement ---
def normalize_budget_label(s):
    if pd.isna(s):
        return ""
    t = str(s).strip()
    # supprimer espaces autour du tiret, enlever espaces inutiles
    t = t.replace(" ", "")
    # standardiser plus/plus de
    t = t.replace("+de", "+de").replace("+De", "+de").replace("plusde", "+de")
    # remplacer variantes comme "+de1000€" -> "+de1000€ (canonical)
    return t

# Canonical keys (sans espaces) et mapping vers l'affichage original
canonical_to_display = {
    "-50€": "-50€",
    "50-100€": "50- 100€",
    "100-200€": "100- 200€",
    "200-300€": "200- 300€",
    "300-400€": "300- 400€",
    "400-700€": "400- 700€",
    "700-1000€": "700- 1000€",
    "+de1000€": "+ de 1000€",
}

# Valeurs moyennes estimées pour chaque canonical key (en €)
canonical_to_value = {
    "-50€": 25,
    "50-100€": 75,
    "100-200€": 150,
    "200-300€": 250,
    "300-400€": 350,
    "400-700€": 550,
    "700-1000€": 850,
    "+de1000€": 1100,
}

# --- Appliquer la normalisation et mapper ---
df_proc = df.copy()

# Normalise : enlève espaces et met en format canonical
df_proc["_budget_norm"] = df_proc["budget_mensuel"].astype(str).apply(lambda x: normalize_budget_label(x))

# On veut transformer ex: "50-100€" vers canonical keys.
# Quelques heuristiques pour reconnaître les formats courants :
def to_canonical(normed):
    if normed == "nan" or normed == "":
        return None
    # remettre le symbole euro si absent (hypothèse)
    # Détecter formes comme "50-100€" ou "50-100" -> ajouter € si besoin
    s = normed
    s = s.replace("EUR", "€")
    # parfois l'utilisateur a gardé le signe '€', parfois non
    # match known patterns
    for key in canonical_to_display.keys():
        # create comparable key without spaces and with € removed for flexible matching
        k_compare = key.replace("€", "").lower()
        s_compare = s.replace("€", "").lower()
        # remove any '+'/ 'de' spacing
        if s_compare == k_compare or s_compare == k_compare.replace("+de", "+de"):
            return key
    # heuristics: if startswith '+' and numbers -> +de1000€
    if s.startswith("+") and "1000" in s:
        return "+de1000€"
    # if pattern like '50-100' or '50-100€'
    import re
    m = re.match(r"^(\d{1,4})-?(\d{1,4})€?$", s)
    if m:
        a = int(m.group(1)); b = int(m.group(2))
        rng = f"{a}-{b}€"
        # map to nearest canonical (handle spaces in canonical keys)
        rng_key = rng.replace("€", "€")
        rng_key = rng_key.replace(" ", "")
        # convert to canonical form like "50-100€"
        cand = f"{a}-{b}€"
        # normalize cand to canonical keys
        cand_norm = cand.replace(" ", "")
        if cand_norm in canonical_to_display:
            return cand_norm
    # fallback: try to remove spaces and match keys (e.g. "50-100€")
    s_nospace = s.replace(" ", "")
    for key in canonical_to_display.keys():
        if s_nospace.lower() == key.replace("€","").lower() or s_nospace.lower() == key.lower():
            return key
    return None

df_proc["_canonical"] = df_proc["_budget_norm"].map(lambda x: to_canonical(x))

# Valeurs non mappées -> on affiche pour debug si nécessaire
non_map = df_proc[df_proc["_canonical"].isna()]["budget_mensuel"].unique()
if len(non_map) > 0:
    st.warning(f"Valeurs de 'budget_mensuel' non reconnues (à vérifier) : {list(non_map)}")

# Colonne d'affichage et colonne numérique estimée
df_proc["budget_display"] = df_proc["_canonical"].map(lambda k: canonical_to_display.get(k) if k is not None else None)
df_proc["budget_estimé"] = df_proc["_canonical"].map(lambda k: canonical_to_value.get(k) if k is not None else np.nan)

# S'assurer de l'ordre des catégories pour l'affichage
df_proc["budget_display"] = pd.Categorical(df_proc["budget_display"], categories=ordre_tranches_display, ordered=True)

# --- Layout : 2 colonnes pour graphiques ---
colA, colB = st.columns([1, 1])

# Graph 1 : répartition empilée (stacked) par situation
with colA:
    cross_counts = (
        df_proc.groupby([col_situation, "budget_display"])
        .size()
        .reset_index(name="count")
    )
    # si aucune valeur dans budget_display, on le signale
    if cross_counts["budget_display"].isna().all():
        st.info("Aucune tranche de budget mappée : vérifie les valeurs de 'budget_mensuel'.")
    fig = px.bar(
        cross_counts,
        x="count",
        y=col_situation,
        color="budget_display",
        orientation="h",
        category_orders={"budget_display": ordre_tranches_display},
        title="Répartition des tranches de budget selon la situation professionnelle",
        labels={"count": "Nombre de répondants", col_situation: "Situation professionnelle", "budget_display": "Budget mensuel"},
    )
    fig.update_layout(title_font_size=18, legend_title_text="Budget")
    st.plotly_chart(fig, use_container_width=True)

# Graph 2 : budget moyen estimé par situation professionnelle
with colB:
    moyenne_par_situation = (
        df_proc.groupby(col_situation)["budget_estimé"]
        .mean()
        .reset_index()
        .rename(columns={"budget_estimé": "budget_moyen"})
        .sort_values("budget_moyen", ascending=False)
    )
    if moyenne_par_situation["budget_moyen"].isna().all():
        st.info("Impossible de calculer le budget moyen : aucune tranche mappée en numérique.")
    fig2 = px.bar(
        moyenne_par_situation,
        x=col_situation,
        y="budget_moyen",
        text=moyenne_par_situation["budget_moyen"].round(0),
        title="Budget mensuel moyen estimé par situation professionnelle (€)",
        labels={col_situation: "Situation professionnelle", "budget_moyen": "Budget moyen (€)"},
    )
    fig2.update_traces(texttemplate="%{text:.0f}€", textposition="outside")
    fig2.update_layout(title_font_size=18, xaxis_tickangle=-20)
    st.plotly_chart(fig2, use_container_width=True)

# --- Grand bloc d'analyse en dessous, plein largeur ---

if not moyenne_par_situation.empty and not moyenne_par_situation["budget_moyen"].isna().all():
    situation_max = moyenne_par_situation.iloc[0]
    situation_min = moyenne_par_situation.iloc[-1]

    texte_analyse = f"""
    <div style="font-size:18px; line-height:1.8; text-align:justify;">
        Le premier graphique montre la répartition des tranches de budget selon la situation professionnelle : il permet de visualiser la proportion de répondants dans chaque tranche de dépense mensuelle pour leur hobby.<br>
        Le second graphique traduit ces tranches en valeurs moyennes estimées, pour comparer directement le budget mensuel moyen par catégorie socio-professionnelle.<br><br>
        On observe que les <b>auto-entrepreneurs et freelances sont ceux qui investissent le plus</b>, avec un budget moyen supérieur à 500 € par mois.<br>
        À l’inverse, les étudiants affichent logiquement les budgets les plus faibles, autour de 170–270 €.<br><br>
        Ce qui est surprenant, c’est que les <b>personnes en recherche d’emploi</b> présentent un budget moyen supérieur à celui des étudiants et même proche des salariés.
    </div>
    """
else:
    texte_analyse = """
    <div style="font-size:18px;">
        Données insuffisantes pour produire une analyse fiable (aucune tranche mappée).
    </div>
    """

st.markdown(texte_analyse, unsafe_allow_html=True)










st.markdown("---") 
# --- TITRE SECTION ---
st.markdown(
    """
    <div style="font-size:20px;">
        <b>Comment évolue la collection selon l'ancienneté ?</b>
    </div>
    """,
    unsafe_allow_html=True
)

# --- PRÉPARATION DES DONNÉES ---

# Exploser les multi-réponses dans collection_type
df_exploded = df.assign(collection_type=df["collection_type"].str.split(",")).explode("collection_type")
df_exploded["collection_type"] = df_exploded["collection_type"].str.strip()

# Croisement ancienneté × type de collection
matrix = pd.crosstab(df_exploded["anciennete_collection"], df_exploded["collection_type"])

# Normalisation pour voir proportions
matrix_prop = matrix.div(matrix.sum(axis=1), axis=0)

# Score d'attraction pour voir quels types de collection attirent selon ancienneté
attraction_scores = matrix.sum(axis=0) / matrix.sum().sum()

attraction_scores = attraction_scores.fillna(0)
attraction_df = attraction_scores.reset_index()
attraction_df.columns = ["Collection_Type", "Attraction_Score"]

# --- VISUALISATIONS ---

# Heatmap proportionnelle
heatmap_fig = px.imshow(
    matrix_prop,
    text_auto=".2f",
    color_continuous_scale="Viridis",
    labels=dict(x="Type de collection", y="Ancienneté dans le hobby", color="Proportion"),
    title="Proportion de collection par ancienneté"
)
heatmap_fig.update_layout(title_font_size=22)

# Barplot attraction
bar_fig = px.bar(
    attraction_df,
    x="Collection_Type",
    y="Attraction_Score",
    text=attraction_df["Attraction_Score"].round(2),
    title="Score d'attraction des types de collection",
    labels={"Collection_Type": "Type de collection", "Attraction_Score": "Score d’attraction"},
)
bar_fig.update_traces(textposition="outside")
bar_fig.update_layout(title_font_size=22, yaxis=dict(range=[0, attraction_df["Attraction_Score"].max() + 0.2]))

# --- STREAMLIT LAYOUT ---
col1, col2, col3 = st.columns([1.3, 1, 1])

with col1:
    st.plotly_chart(heatmap_fig, use_container_width=True)

with col2:
    st.plotly_chart(bar_fig, use_container_width=True)

with col3:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Cette heatmap montre comment chaque <b>ancienneté dans le hobby</b> se répartit sur les différents types de collection.<br><br>
        Le <b>score d’attraction</b> (graphique de droite) indique quels types de collection sont les plus “populaires” toutes anciennetés confondues :<br><br>
        • Un score élevé = type de collection qui attire beaucoup de collectionneurs, indépendamment de leur ancienneté.<br>
        • Un score faible = type plus niche ou spécifique à certaines tranches d’ancienneté.<br><br>
        Ces visualisations permettent d’identifier si certains types de collection sont réservés aux vétérans ou attirent tous les profils.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

# --- CHAMP POUR ANALYSE AUTOMATIQUE ---
# Préparer un texte automatique (exemple basique)
top_collection = attraction_df.sort_values("Attraction_Score", ascending=False).iloc[0]["Collection_Type"]
commentaire_auto = f"""
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    Le type de collection le plus attractif est <b>{top_collection}</b>, ce qui signifie qu’il attire beaucoup de collectionneurs, quel que soit leur niveau d’ancienneté.<br>
    À l’inverse, certains types comme {', '.join(attraction_df.sort_values("Attraction_Score").head(2)["Collection_Type"].tolist())} semblent plus spécifiques à certaines tranches d’ancienneté.
</div>
"""
st.markdown(commentaire_auto, unsafe_allow_html=True)








st.markdown("---") 

# --- ANALYSE : Profil du collectionneur selon âge, ancienneté et budget ---

st.markdown(
    """
    <div style="font-size:20px;">
        <b>Profil du collectionneur selon âge, ancienneté et budget</b>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Nettoyage & préparation des données ---
df_analyse = df.copy()

# Conversion budget en numérique si besoin (ex: "Moins de 50€", "50-100€", etc.)
budget_map = {
    "-50€": 25,
    "50- 100€": 75,
    "100- 200€": 150,
    "200- 300€":250,
    "300- 400€": 350,
    "400- 700":550,
    "700- 1000":850,
    "+ de 1000€": 1300
}
df_analyse["budget_val"] = df_analyse["budget_mensuel"].map(budget_map).fillna(0)

# Remplacement des catégories d’ancienneté et âge par un ordre cohérent si nécessaire
age_order = ["Moins de 14 ans", "14 - 18 ans", "18 - 22 ans", "22 - 26 ans", "26 - 30 ans", "30 - 35 ans","+ 35 ans"]
anciennete_order = ["-1 an", "1 à 2 ans", "2 à 4 ans", "4 à 6 ans", "6 ans ou +"]

df_analyse["age"] = pd.Categorical(df_analyse["age"], categories=age_order, ordered=True)
df_analyse["anciennete_collection"] = pd.Categorical(df_analyse["anciennete_collection"], categories=anciennete_order, ordered=True)

# --- Heatmap Âge x Ancienneté ---
heatmap_data = (
    df_analyse.groupby(["age", "anciennete_collection"])["budget_val"]
    .mean()
    .unstack()
)

heatmap_fig = px.imshow(
    heatmap_data,
    color_continuous_scale="Blues",
    text_auto=".1f",
    title="Budget moyen selon âge et ancienneté",
    labels=dict(color="Budget moyen (€)"),
)
heatmap_fig.update_layout(title_font_size=22)

# --- Barplot Budget moyen par investisseur ---
bar_data = (
    df_analyse.groupby("investisseur")["budget_val"]
    .mean()
    .reset_index()
    .sort_values(by="budget_val", ascending=False)
)

bar_fig = px.bar(
    bar_data,
    x="investisseur",
    y="budget_val",
    text=bar_data["budget_val"].round(0),
    color="budget_val",
    color_continuous_scale="Viridis",
    title="Budget moyen selon le statut d’investisseur",
    labels={"investisseur": "Investisseur", "budget_val": "Budget moyen (€)"},
)
bar_fig.update_traces(textposition="outside")
bar_fig.update_layout(title_font_size=22, showlegend=False)

# --- Affichage Streamlit ---
col1, col2, col3 = st.columns([1.3, 1, 1])

with col1:
    st.plotly_chart(heatmap_fig, use_container_width=True)

with col2:
    st.plotly_chart(bar_fig, use_container_width=True)

with col3:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Cette heatmap illustre comment le <b>budget moyen</b> évolue selon les <b>tranches d’âge</b> et 
        <b>l’ancienneté de collection</b>.<br><br>
        On observe si les collectionneurs les plus expérimentés ou plus âgés 
        dépensent davantage, ou si les nouveaux arrivants sont plus impulsifs.<br><br>
        Le graphique de droite montre la différence entre <b>investisseurs</b> et 
        <b>collectionneurs passion</b>.<br><br>
        Une différence nette suggère une <b>segmentation économique</b> claire entre les profils.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

# --- Analyse automatique / texte ---
moy_invest = bar_data.loc[bar_data["investisseur"] == "Oui", "budget_val"].mean()
moy_noninvest = bar_data.loc[bar_data["investisseur"] != "Oui", "budget_val"].mean()

analyse_auto = f"""
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    On observe une <b>corrélation positive entre l’ancienneté et le budget</b>, 
    surtout à partir de <b>2 ans d’ancienneté</b>.<br>
    Les collectionneurs ayant plus de <b>6 ans d’expérience</b> affichent les budgets les plus élevés 
    (par ex. <b>385 €</b>, <b>412 €</b>, <b>455 €</b> selon les tranches d’âge).<br><br>
    Certains pics atypiques, comme les <b>662 € chez les moins de 14 ans</b>, 
    s’expliquent probablement par un <b>faible effectif</b> dans cette catégorie et sont donc à interpréter avec prudence.<br>
    Globalement, les <b>18–30 ans</b> constituent la tranche la plus active budgétairement, 
    souvent associée à un profil <b>“passion + moyens”</b>.<br>
    Les <b>investisseurs affirmés</b> (oui à 100 %) présentent le <b>budget moyen le plus élevé</b> 
    (≈ <b>256 €</b>), suivis des profils <b>“mixtes”</b> (≈ <b>241 €</b>) qui équilibrent 
    entre plaisir et revente.<br>
    Les <b>non-investisseurs</b> restent nettement en dessous, avec un budget autour de <b>150 €</b>, 
    soit <b>presque moitié moins</b> que les investisseurs.
</div>
"""
st.markdown(analyse_auto, unsafe_allow_html=True)







st.markdown("---") 

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prince import MCA

# --- TITRE ---
st.markdown(
    """
    <div style="font-size:20px;">
        <b>Analyse des goûts selon la génération d’entrée</b>
    </div>
    """,
    unsafe_allow_html=True
)

# --- CHARGEMENT DES DONNÉES ---
colonnes = ["gen_arrivee", "gen_preferee", "bloc_prefere", "jeu_prefere_principal"]
df_acm = df[colonnes].dropna()

# --- ANALYSE DES CORRESPONDANCES MULTIPLES (ACM) ---
mca = MCA(n_components=2, random_state=42)
mca_fit = mca.fit(df_acm)

# Coordonnées des modalités
coords_modalites = mca_fit.column_coordinates(df_acm)
coords_modalites["variable"] = [col.split("_")[0] for col in coords_modalites.index]
coords_modalites["modalite"] = [col for col in coords_modalites.index]

# --- VISUALISATION ---
fig, ax = plt.subplots(figsize=(9, 7))
palette = {
    "gen": "#ff7f0e",
    "bloc": "#2ca02c",
    "jeu": "#1f77b4"
}

for var, data in coords_modalites.groupby("variable"):
    ax.scatter(data[0], data[1], label=var, alpha=0.8, s=60, c=palette.get(var, "#7f7f7f"))

for i, row in coords_modalites.iterrows():
    ax.text(row[0] + 0.02, row[1], row["modalite"], fontsize=9)

ax.axhline(0, color="gray", lw=1)
ax.axvline(0, color="gray", lw=1)
ax.set_title("Analyse des Correspondances Multiples (ACM)\nGénérations, blocs et jeux préférés", fontsize=14)

# --- RÉCUPÉRATION DE LA VARIANCE EXPLIQUÉE ---
try:
    inertia = mca_fit.explained_inertia_
except AttributeError:
    try:
        inertia = mca_fit.explained_inertia()
    except Exception:
        # fallback manuel
        eigenvalues = mca_fit.eigenvalues_
        inertia = eigenvalues / eigenvalues.sum()

ax.set_xlabel(f"Dimension 1 ({inertia[0]*100:.1f}%)")
ax.set_ylabel(f"Dimension 2 ({inertia[1]*100:.1f}%)")
ax.legend(title="Variable", bbox_to_anchor=(1.05, 1), loc='upper left')
sns.despine()
st.pyplot(fig)

# --- INTERPRÉTATION ---
st.markdown("### Aide à l'interprétation :")

analyse_auto = f"""
<div style="font-size:20px; line-height:1.6;">
    - Les points proches représentent des choix similaires (par ex. ceux arrivés à la 4G préfèrent souvent les jeux ou blocs de cette période).  <br>
    - L’axe 1 (horizontal) peut traduire un gradient temporel (vintage → récent),  <br>
    - L’axe 2 (vertical) peut montrer des différences de styles ou d’attachement générationnel. 
</div>
"""
st.markdown(analyse_auto, unsafe_allow_html=True)

# --- VARIANCE EXPLIQUÉE ---
st.markdown(f"**Variance expliquée :** {inertia[0]*100:.1f}% par la Dim 1 et {inertia[1]*100:.1f}% par la Dim 2.")
analyse_auto = f"""
<div style="font-size:20px; line-height:1.6;">
    L'analyse rapide : la 4G, la 5G et la 6G sont à part, mais le reste des blocs se maintiennent entre eux (1-2-3G)
</div>
"""
st.markdown(analyse_auto, unsafe_allow_html=True)





st.markdown("---") 

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Transformation des tranches en valeurs numériques ---
boosters_map = {
    "Entre 0 et 5 boosters": 2.5,
    "+ de 5 boosters": 10,
    "+ de 15 boosters": 22.5,
    "+ de 30 boosters": 40,
    "+ de 50 boosters": 75,
    "+ de 100 boosters": 120
}

investissements_map = {
    "-100€": 50,
    "100 - 300€": 200,
    "300 - 500€": 400,
    "500 - 1000€": 750,
    "1000 - 2000€": 1500,
    "2000 - 5000€": 3500,
    "5000 - 10000€": 7500,
    "+ de 10000€": 13000
}

# --- Création des colonnes numériques ---
df["boosters_num"] = df["boosters_par_mois"].map(boosters_map).fillna(0)
df["valeur_investissements_num"] = df["valeur_investissements"].map(investissements_map).fillna(0)

# --- Regroupement pour comptage des répondants ---
scatter_df = df.groupby(["boosters_num", "valeur_investissements_num", "investisseur"]) \
               .size().reset_index(name='nb_repondants')

# --- Scatter plot ---
scatter_fig = px.scatter(
    scatter_df,
    x="boosters_num",
    y="valeur_investissements_num",
    size="nb_repondants",
    color="investisseur",
    labels={
        "boosters_num": "Boosters ouverts par mois",
        "valeur_investissements_num": "Valeur estimée des investissements (€)",
        "investisseur": "Type d'investisseur",
        "nb_repondants": "Nombre de répondants"
    },
    title="Comportement d'ouverture vs investissement",
    size_max=25  # taille max des bulles
)
scatter_fig.update_layout(title_font_size=22)

# --- Streamlit layout ---
st.markdown(
    """
    <div style="font-size:20px;">
        <b>Comportement d’ouverture vs investissement</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.plotly_chart(scatter_fig, use_container_width=True)

# --- Commentaire ---
commentaire = """
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    Chaque point représente une combinaison entre le <b>nombre de boosters ouverts par mois</b> 
    et la <b>valeur estimée des investissements</b>.  
    La <b>taille des points</b> indique le nombre de répondants correspondant à chaque profil observé.<br><br>
    On observe une forte concentration de <b>non-investisseurs</b> (en bleu) dans la partie 
    inférieure gauche du graphique : ils dépensent peu et ouvrent un nombre limité de boosters, 
    traduisant une pratique plus <b>loisir ou occasionnelle</b> du TCG.<br><br>
    À l’inverse, les <b>profils investisseurs</b> (en rouge) présentent logiquement des <b>valeurs d’investissement plus élevées</b>.  
    Toutefois, même parmi eux, l’ouverture mensuelle reste <b>modérée</b> — 
    rarement au-delà de <b>30 boosters par mois</b> — suggérant une approche plus <b>sélective et orientée vers la revente</b> plutôt que la consommation massive.<br><br>
    Ce graphique met donc en évidence <b>deux comportements bien distincts</b> :  
    une majorité de collectionneurs plaisir, et une minorité d’investisseurs.
</div>
"""
st.markdown(commentaire, unsafe_allow_html=True)






st.markdown("---") 

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Conversion des avis textuels en scores ---
avis_mapping = {
    "Très mauvais": 1,
    "Plutôt mauvais": 2,
    "Plutôt bon": 3,
    "Très bon": 4
}

# Colonnes d'avis pour les conventions
avis_cols = [
    "avis_convention_prix",
    "avis_convention_exposants",
    "avis_convention_importance",
    "avis_convention_dispo",
    "avis_convention_tarifs",
    "avis_convention_securite"
]

# Transformation en scores numériques
for col in avis_cols:
    df[col + "_score"] = df[col].map(avis_mapping)

# Calcul de la moyenne par critère
radar_data = pd.DataFrame({
    "Critère": ["Prix d'entrée", "Qualité des exposants", "Importance", 
                "Disponibilité des produits", "Tarifs sur place", "Sécurité"],
    "Score moyen": [df[col + "_score"].mean() for col in avis_cols]
})

# --- Graphique radar ---
radar_fig = px.line_polar(
    radar_data,
    r="Score moyen",
    theta="Critère",
    line_close=True,
    markers=True,
    title="Perception moyenne des conventions TCG"
)
radar_fig.update_traces(fill='toself')
radar_fig.update_layout(title_font_size=22, polar=dict(radialaxis=dict(range=[1,4])))

# --- Streamlit layout ---
st.markdown(
    """
    <div style="font-size:20px;">
        <b>Expérience convention TCG et perception</b>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.plotly_chart(radar_fig, use_container_width=True)

with col2:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Ce radar montre la perception moyenne des conventions TCG Pokémon selon différents critères.<br><br>
        • Chaque axe correspond à un critère évalué : <b>Prix d'entrée</b>, <b>Qualité des exposants</b>, 
          <b>Importance</b>, <b>Disponibilité des produits</b>, <b>Tarifs sur place</b>, <b>Sécurité</b>.<br>
        • Les scores vont de 1 (Très mauvais) à 4 (Très bon).<br><br>
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

# --- Analyse automatique ---
analyse = f"""
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    Scores moyens par critère :<br>
    • <b>Prix d'entrée</b> : {radar_data.loc[radar_data['Critère']=="Prix d'entrée", 'Score moyen'].values[0]:.2f} / 4<br>
    • <b>Qualité des exposants</b> : {radar_data.loc[radar_data['Critère']=="Qualité des exposants", 'Score moyen'].values[0]:.2f} / 4<br>
    • <b>Importance</b> : {radar_data.loc[radar_data['Critère']=="Importance", 'Score moyen'].values[0]:.2f} / 4<br>
    • <b>Disponibilité des produits</b> : {radar_data.loc[radar_data['Critère']=="Disponibilité des produits", 'Score moyen'].values[0]:.2f} / 4<br>
    • <b>Tarifs sur place</b> : {radar_data.loc[radar_data['Critère']=="Tarifs sur place", 'Score moyen'].values[0]:.2f} / 4<br>
    • <b>Sécurité</b> : {radar_data.loc[radar_data['Critère']=="Sécurité", 'Score moyen'].values[0]:.2f} / 4<br><br>
</div>
"""
st.markdown(analyse, unsafe_allow_html=True)

analyse_auto = """
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    En moyenne, les conventions TCG obtiennent des <b>notes globalement positives</b>, 
    avec des scores compris entre <b>2.1 et 3.5 sur 4</b>.<br><br>
    Les participants jugent particulièrement bien :<br>
    • <b>l’importance</b> de ces conventions (<b>3.46 / 4</b>), signe qu’elles sont perçues comme essentielles dans la communauté.<br>
    • <b>la qualité des exposants</b> (<b>3.08 / 4</b>) et la <b>disponibilité des produits</b> (<b>3.02 / 4</b>), 
    ce qui traduit une offre variée et satisfaisante.<br><br>
    En revanche, certains points méritent d’être améliorés :<br>
    • <b>les tarifs sur place</b> (<b>2.12 / 4</b>) sont perçus comme trop élevés par de nombreux visiteurs.<br>
    • <b>la sécurité</b> obtient la note la plus faible (<b>2.10 / 4</b>), 
    ce qui peut refléter un sentiment de manque de contrôle ou d’organisation dans les grands événements.<br><br>
    Enfin, le <b>prix d’entrée</b> reste jugé plutôt correct (<b>2.73 / 4</b>), 
    plaçant le rapport qualité-prix dans une zone acceptable.<br><br>
</div>
"""
st.markdown(analyse_auto, unsafe_allow_html=True)

