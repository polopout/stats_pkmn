import streamlit as st
import plotly.express as px
from utils.data import load_data, clean_and_count_column, normalize_card_name
from utils.viz import generic_multi_bar, generic_bar, generic_pie, wordcloud_plot, sidebar_logo
from collections import Counter
import pandas as pd
import re
import os


sidebar_logo()
 
# st.plotly_chart(generic_pie(df, "serie_preferee_wizard"), use_container_width=True)
# st.plotly_chart(generic_multi_bar(df, "jeux_principaux", sep=",", horizontal=True, top_n=10), use_container_width=True)
# st.plotly_chart(generic_bar(df, "anciennete_collection", title="Bar anciennete_collection"), use_container_width=True)

st.set_page_config(page_title="Votre collection", page_icon="📁", layout="wide")


st.title("Quel est le contenu de votre collection ?")
st.markdown(
    """
    <div style="font-size:20px;">
        Troisième partie - Dans cette section nous allons revenir sur le contenu de votre collection, cartes et séries préférées, ...
    </div>
    """,
    unsafe_allow_html=True
)
df = load_data()



col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.plotly_chart(generic_pie(df, "serie_preferee_wizard", title="Série Wizard preférée"), use_container_width=True)
with col2:
    st.plotly_chart(generic_pie(df, "serie_preferee_ex", title="Série Ex preférée"), use_container_width=True)
with col3:
    st.plotly_chart(generic_pie(df, "serie_preferee_dp", title="Série DP preférée"), use_container_width=True)

col4, col9, col5 = st.columns([1, 1, 1])

with col4:
    st.plotly_chart(generic_pie(df, "serie_preferee_platine", title="Série Platine preférée"), use_container_width=True)
with col9:
    st.plotly_chart(generic_pie(df, "serie_preferee_hgss", title="Série HGSS preférée"), use_container_width=True)
with col5:
    st.plotly_chart(generic_pie(df, "serie_preferee_nb", title="Série NB preférée"), use_container_width=True)

col6, col7, col8 = st.columns([1, 1, 1])

with col6:
    st.plotly_chart(generic_pie(df, "serie_preferee_xy", title="Série XY preférée"), use_container_width=True)
with col7:
    st.plotly_chart(generic_pie(df, "serie_preferee_sl", title="Série SL preférée"), use_container_width=True)
with col8:
    st.plotly_chart(generic_pie(df, "serie_preferee_eb", title="Série EB preférée"), use_container_width=True)

col10, col11, col111 = st.columns([1, 1,1])
with col10:
    st.plotly_chart(generic_pie(df, "serie_preferee_ev", title="Série EV preférée"), use_container_width=True)
with col11:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Pas de grosses surprises dans les séries préférées par bloc. On retrouve les classiques <b>Zénith Supreme et 151</b> pour le plus récent, et du <b>Aquapolis et Deoxys</b> pour le plus vintage.
        <br><br>Idem pour les blocs préférés, il n'est pas surprenant de trouver <b>Wizard et Ex</b> en tête du classement, ainsi que EV pas loin. Pour moi les surprises sont le bloc HGSS ainsi que EB, que j'aurai bien vu à des places plus opposées.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)
with col111:
    st.plotly_chart(generic_pie(df, "bloc_prefere", title="Bloc préféré"), use_container_width=True)





st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Centre de la collection
    </div>
    """,
    unsafe_allow_html=True
)



col20, colaz, col21 = st.columns([1,1,1])
with col20:
    st.plotly_chart(generic_multi_bar(df, "collection_type", sep=",", horizontal=False, title="Type de collection",legend_title = {"x": "Type de collection", "y": "Nombre de votes"}), use_container_width=True)
with colaz:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Evidemment les <b>cartes en lose</b> prennent la première place, mais on pourrait être surpris de trouver <b>le scellé</b> si haut avec 77 votants. Un autre choix de collection qui a été suggéré était le vide.
        <br><br>Pour ce qui s'agit des collections des cartes, ce sont <b>les coups de coeur</b> qui mènent la danse, suivi de près par les <b>full-set et les full-set de Pokémon</b>.<br>
        D'autres catégories ont été suggérées : Waifus, Grosses cartes, TG-GG, Fossiles, Raretés etc.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)
with col21:
    st.plotly_chart(generic_multi_bar(df, "non_grade_collection", sep=",", horizontal=False, title="Comment collectionnez-vous les cartes ?",legend_title = {"x": "Format de collection de cartes", "y": "Nombre de votes"}), use_container_width=True)







st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Le scellé
    </div>
    """,
    unsafe_allow_html=True
)

col22, col23 = st.columns([1,1])


with col22:
   #st.plotly_chart(generic_multi_bar(df, "scelle_type", sep=",", horizontal=False, protected_groups=["Du récent (EV, EB)","Du semi-vintage (SL, XY, NB)","Du vintage (Wizard, Ex, DPP, HGSS)"]), use_container_width=True)
   st.plotly_chart(generic_multi_bar(df,"scelle_type",sep=",",horizontal=False,protected_groups=["Du récent (EV, EB)","Du semi-vintage (SL, XY, NB)","Du vintage (Wizard, Ex, DPP, HGSS)"],top_n=10,title_font_size=22,legend_title={"x": "Nombre de votes", "y": "Type de scellé"}),use_container_width=True)

with col23:
    st.plotly_chart(generic_bar(df, "valeur_scelle", title="Bar valeur_scelle",legend_title={"x": "Nombre de votes", "y": "Valeur du scellé"}), use_container_width=True)

col24, col25 = st.columns([1,1])
with col24:
    commentaire = """
    <div style="font-size:19px; line-height:1.6;">
        <br><br>
        Concernant le scellé, beaucoup expriment une crainte forte autour de son avenir.<br>
        Des craintes autour de <b>manipulations de marché</b> ainsi que de <b>bulles spéculatives</b> ressortent particulièrement.<br><br>
        Tout le monde semble s'accorder sur le fait que le scellé récent prendra en valeur, mais probablement moins que le vintage à cause d'un <b>surstock</b>.<br><br>
        A noter l'agacement de certains sur le fait que les enfants ne pourront pas avoir de souvenirs en lien avec les ouvertures dû au scalping.<br><br>
        Enfin une minorité est contente du scellé vintage car il <b>laisse place aux émotions de l'enfance</b> lors de la redécouverte des items en question.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with col25:

    data = [
        ("Récent surstocké → chute ?", 19),
        ("Plus d'ancien tout sera ouvert", 3),
        ("Contre", 16),
        ("Prendra en valeur", 21),
        ("Récent ne va pas monter autant que le vintage", 5),
        ("Peur du recollé / rescellé (confiance)", 21),
        ("Décorrélation vintage / récent", 3),
        ("Montre l'importance de la licence", 4),
        ("Pb trouver items en magasin (scalping, enfants)", 17),
        ("Cool pour trouver du vintage enfance", 2),
        ("Investissement > beauté", 3)
    ]

    df_points = pd.DataFrame(data, columns=["avis", "points"])

    fig = px.bar(
        df_points,
        x="avis",
        y="points",        # <- correction ici
        text="points",     # <- correction ici aussi
        title="Avis sur l'avenir du scellé dans Pokémon",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Avis",
        yaxis_title="Nombre de votes",
        title_font_size=24,
        xaxis_tickangle=-30
    )

    st.plotly_chart(fig, use_container_width=True)




st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Le gradé
    </div>
    """,
    unsafe_allow_html=True
)


col28963, col289633 = st.columns([2,1])
with col28963:
    st.plotly_chart(generic_multi_bar(df, "societes_gradation_appreciees", sep=",", horizontal=False,legend_title={"x": "Nombre de votes", "y": "Sociétés de gradation"},title="Quelles sont les sociétés de gradation les plus appréciées ?"), use_container_width=True)
with col289633:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Le top des sociétés préférées des votants sont <b>CCC, PSA, CollectAura ainsi que PCA</b> en grands leaders.<br>
        Ce résultat est surprenant lorsqu'on constate que CCC n'apparaît qu'en 4e position des sociétés chez qui les gens ont gradé, bien derrière  <b>PCA et PSA qui se retrouvent à égalité en première position </b>.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

col28, col29, col30 = st.columns([1,2,2])
with col28:
    st.plotly_chart(generic_pie(df, "grade",title="Possédez-vous des cartes gradées ?"), use_container_width=True)
with col29:
    st.plotly_chart(generic_multi_bar(df, "societe_gradation", sep=",", horizontal=False,legend_title={"x": "Nombre de votes", "y": "Sociétés de gradation"},title="Chez quelles sociétés avez-vous déjà gradé ?"), use_container_width=True)
with col30:
    st.plotly_chart(generic_multi_bar(df, "Colonne 24", sep=",", horizontal=False,legend_title={"x": "Nombre de votes", "y": "Raison pour grader"},title="Répartition des raisons de la gradation"), use_container_width=True)


col24321, col25321 = st.columns([1,1])
with col24321:
    commentaire = """
    <div style="font-size:19px; line-height:1.6;">
        <br><br>
        Selon une majorité, le gradé à <b>un avenir prometteur</b> (40 votes) contre une majorité qui estime que son avenir est mitigé (10 votes).<br>
        Les raisons qui reviennent sont des inquiétudes vis-à-vis des<b> faux boitiers</b> qui inondent le marché actuel, ainsi que de tous les dramas associés aux sociétés de gradation.<br><br>
        Beaucoup relèvent aussi le <b>côté pratique</b> de la gradation qui offre des protections anti UV, anti humidité, et le futur de la gradation a été évoqué, la gradation par intelligence artificielle a été évoquée plusieurs fois.<br><br>
        Pour finir certains estiment que l'avenir de la gradation n'est lié qu'à l'<b>investissement au détriment de la beauté</b> et de la protection.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with col25321:

    data = [
        ("Prometteur / Bon avenir", 40),
        ("Mitigé / Incertain", 10),
        ("Inquiétant / Problèmes", 15),
        ("Pas d’avis / Ne sais pas", 8),
        ("Investissement / spéculation", 12),
        ("Technique / pratique", 18),
        ("IA / futur tech", 5)
    ]

    df_points2 = pd.DataFrame(data, columns=["avis", "points"])

    fig = px.bar(
        df_points2,
        x="avis",
        y="points",        # <- correction ici
        text="points",     # <- correction ici aussi
        title="Avis sur l'avenir du scellé dans Pokémon",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Avis",
        yaxis_title="Nombre de votes",
        title_font_size=24,
        xaxis_tickangle=-30
    )

    st.plotly_chart(fig, use_container_width=True)





st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Raretés préférées
    </div>
    """,
    unsafe_allow_html=True
)

col31, col32, col33 = st.columns([1,1,1])
with col31:
    st.plotly_chart(generic_bar(df, "rarete_vintage_preferee", title="Rareté vintage préférée",legend_title={"x": "Nombre de votes", "y": "Type de raretés"}), use_container_width=True)
with col32:
    st.plotly_chart(generic_bar(df, "rarete_semivintage_preferee", title="Rareté semi-vintage préférée",legend_title={"x": "Nombre de votes", "y": "Type de raretés"}), use_container_width=True)
with col33:
    st.plotly_chart(generic_bar(df, "rarete_recente_preferee", title="Rareté récente préférée",legend_title={"x": "Nombre de votes", "y": "Type de raretés"}), use_container_width=True)





st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Carte préférée du TCG
    </div>
    """,
    unsafe_allow_html=True
)


df["carte_preferee_normalisee"] = df["carte_preferee"].dropna().apply(normalize_card_name)

# Compter occurrences
counts = df["carte_preferee_normalisee"].value_counts().reset_index()
counts.columns = ["carte", "nb_votes"]

# Top 3
top3 = counts.head(10)


IMAGE_FOLDER = "stats_pkmn\\data"  # ton dossier avec les visuels

import os

cols = st.columns(10)
for n, (i, row) in enumerate(top3.iterrows(), start=1):
    card = row["carte"]

    # Vérifie si le fichier existe en jpeg ou png
    filepath = None
    for ext in [".jpg", ".png"]:
        filename = card + ext
        candidate = os.path.join(IMAGE_FOLDER, filename)
        if os.path.exists(candidate):
            filepath = candidate
            break

    with cols[n-1]:  # car enumerate démarre à 1
        if filepath:
            with st.expander(f"Cliquez pour révéler le Top {n} 👀"):
                st.image(filepath, caption=f"{card} ({row['nb_votes']} votes)", use_container_width=True)
        else:
            st.write(f"Top {n} : {card} ({row['nb_votes']} votes) - ❌ Pas d'image trouvée")





