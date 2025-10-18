import streamlit as st
from utils.data import load_data, clean_and_count_column
from utils.viz import generic_multi_bar, generic_bar, generic_pie, wordcloud_plot, sidebar_logo, generic_multi_pie
import plotly.express as px


sidebar_logo()

st.set_page_config(page_title="Vous et Pokémon", page_icon="🧑‍🤝‍🧑", layout="wide")

st.title("Votre relation avec Pokémon")
st.markdown(
    """
    <div style="font-size:20px;">
        Seconde partie - Dans cette section nous allons revenir sur votre rapport avec Pokémon de manière très générale.
    </div>
    """,
    unsafe_allow_html=True
)
df = load_data()




col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.plotly_chart(generic_bar(df, "anciennete_collection", title="Répartition de l'ancienneté dans Pokémon",legend_title = {"x": "Ancienneté dans Pokémon", "y": "Nombre de votes"}), use_container_width=True)
with col2:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Une majorité des personnes collectionnent ou ont repris la collection depuis <b>6 ans ou plus</b>, et une tendance se dégage : le hobby continue d'intéresser.<br><br>
        <b>Encore 10 personnes sont arrivées dans la collection cette année ! </b>
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)



with col3:
    st.plotly_chart(generic_pie(df, "professionnel", title="Etes-vous professionnel ?"), use_container_width=True)







st.markdown("---")

col4, col5 = st.columns([2, 1])
with col4:
    st.plotly_chart(generic_multi_pie(df, "porte_entree", title="Répartition des portes d'entrée des collectionneurs dans Pokémon", sep=","))
with col5:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        On est quasiment sur du trois fois <b>1/3 entre les cartes, l'animé et les jeux-vidéos</b>.<br><br>
        Une personne m'a aussi cité le fait qu'il était revenu dans les cartes grâce à son fils, et un autre par les goodies.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)





st.markdown("---") 

col6, col7 = st.columns([2, 1])
with col6:
    st.plotly_chart(generic_multi_bar(df, "jeux_principaux",title="Jeux de la lignée principale les plus joués", sep=",",legend_title = {"x": "Jeux lignée principale", "y": "Nombre de votes"}), use_container_width=True) 
with col7:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        On constate que les jeux sortis à l'<b>époque de 4G - 5G</b> sont ceux qui ont été les plus joués, donc <b>entre 2007 et 2012</b>.<br><br>
        Ensuite dans le classement on a les jeux "récents", et logiquement les jeux les plus vieux ensuite, car on est sur des générations plus anciennes.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)




st.markdown("---") 

col8, col9 = st.columns([2, 1])
with col8:
    st.plotly_chart(generic_multi_bar(df, "jeux_hors_lignee",title="Jeux hors lignée principale les plus joués", sep=",",legend_title = {"x": "Jeux hors lignée principale", "y": "Nombre de votes"}), use_container_width=True) 
with col9:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Les jeux récents sur mobile sont évidemments les jeux auquel tout le monde à joué : <b>PoGo et Pokémon tcg Pocket</b>.<br><br>
        Le petit chouchou qui arrive troisème est un des jeux préféré des fans de Pokémon : <b>Pokémon Donjon Mystère</b>. 
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)


st.markdown("---")  

df_counts = clean_and_count_column(df, "pokemon_favoris") 
top_counts = df_counts.head(10)

fig = px.bar(
    top_counts,
    x="word",
    y="count",
    text="count",
    title="Top 10 des Pokémon qui reviennent le plus :",
    labels={"word": "Pokémon", "count": "Nombre de votes"}  # <-- renommer les axes
)

fig.update_traces(textposition="outside")

# Affichage dans Streamlit
col10, col11 = st.columns([1, 1])
with col10:
    st.plotly_chart(fig, use_container_width=True)

with col11:
    plt = wordcloud_plot(df_counts, column="word", title="")
    st.pyplot(plt)




st.markdown("---") 

col12, col13 = st.columns([2, 1])

with col12:
    st.plotly_chart(generic_bar(df, "gen_preferee", title="Génération préférée des collectionneurs",legend_title = {"x": "Génération préférée", "y": "Nombre de votes"}), use_container_width=True)
with col13:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Sans surprise maintenant que l'on sait que les jeux de la 4g ont été les plus joués, <b>Diamant et Perle, la quatrième génération</b> est logiquement la génération préférée des collectionneurs.<br><br>
        On peut aussi notifier que la 7G n'a été choisie par personne !
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)