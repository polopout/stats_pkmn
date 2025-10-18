import streamlit as st
from utils.data import load_data, load_geojson, count_departements
from utils.viz import generic_pie, plot_dept_map, generic_bar, sidebar_logo
from streamlit_folium import st_folium

sidebar_logo()

st.set_page_config(page_title="Qui êtes-vous ?", page_icon="❓", layout="wide")

st.title("Qui êtes vous ?")
st.markdown(
    """
    <div style="font-size:20px;">
        Première partie - Nous allons voir dans cette partie quel est le profil moyen d'un collectionneur de cartes Pokémon en France.
    </div>
    """,
    unsafe_allow_html=True
)

df = load_data()

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(generic_bar(df, "genre", title="Répartition par genres",legend_title = {"x": "Genres", "y": "Nombre de votes"}), use_container_width=True)
with col2:
    st.plotly_chart(generic_bar(df, "situation", title="Répartition par situations professionelles",legend_title = {"x": "Situation pro", "y": "Nombre de votes"}), use_container_width=True)

st.markdown("---")  

col3, col4 = st.columns([1, 1]) 
with col3:
    st.plotly_chart(generic_pie(df, "age", title="Répartition par tranche d'âges"), use_container_width=True)
with col4:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        On voit clairement une <b>forte majorité d’hommes (123)</b> parmi les répondants, contre seulement 13 femmes et 1 personne non-binaire, 
        ce qui confirme que la <b>communauté Pokémon TCG reste très masculine</b>.<br><br>
        Côté situation, les <b>salariés en CDI (53)</b> et les <b>étudiants en études supérieures (38)</b> représentent les deux groupes principaux, 
        ce qui suggère une population relativement jeune mais déjà active ou en formation.<br><br>
        La répartition par âge montre que les <b>22-26 ans dominent</b> (37,2 %), <b>suivis des 26-30 ans</b> (19 %), 
        ce qui place la majorité des collectionneurs dans la vingtaine.<br><br>
        Les 18-22 ans (18,2 %) constituent aussi une part significative, tandis que les plus jeunes (14-18 ans) et les plus de 35 ans restent minoritaires.
        On peut en déduire que le cœur de la communauté est composé de <b>jeunes adultes</b>, probablement arrivés dans Pokémon dans leur enfance 
        et qui poursuivent leur passion à l’âge adulte avec davantage de moyens financiers.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)



st.markdown("---")  

col5, col6 = st.columns([2,1])
gdf = load_geojson()


with col5:
    dept_counts = count_departements(df)
    m = plot_dept_map(gdf, dept_counts)
    st_folium(m, width=1000, height=800)

with col6:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br><br>
        Les zones qui présentent le plus de collectionneurs semblent être <b>l'Ouest de la France</b>, ainsi que <b>le Nord</b>, et plus globalement les métropoles françaises.<br><br>
        A noter qu'il y a aussi des personnes qui ne sont pas en France, on m'a aussi coté Bali, le Maroc, la Belgique ou la Suisse !
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)