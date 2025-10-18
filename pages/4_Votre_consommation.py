import streamlit as st
from utils.data import load_data, clean_and_count_column
from utils.viz import generic_multi_bar, generic_bar, generic_pie, generic_multi_pie, wordcloud_plot, sidebar_logo
import plotly.express as px
import pandas as pd

sidebar_logo()
 
# st.plotly_chart(generic_pie(df, "serie_preferee_wizard"), use_container_width=True)
# st.plotly_chart(generic_multi_bar(df, "jeux_principaux", sep=",", horizontal=True, top_n=10), use_container_width=True)
# st.plotly_chart(generic_bar(df, "anciennete_collection", title="Bar anciennete_collection"), use_container_width=True)
# st.plotly_chart(generic_multi_pie(df, "ta_colonne", sep=",", protected_groups=["Du récent (EV, EB)","Du semi-vintage (SL, XY, NB)"]))

st.set_page_config(page_title="Votre consommation", page_icon="💵", layout="wide")


st.title("Comment consommez vous Pokémon ?")
st.markdown(
    """
    <div style="font-size:20px;">
        Quatrième partie - Dans cette section nous allons parler d'argent, de lieux qui alimentent notre passion commune, des différents services que nous sommes amenés à utiliser ainsi que des influenceurs Pokémon en France.
    </div>
    """,
    unsafe_allow_html=True
)
df = load_data()



st.markdown("---")  

st.markdown(
    """
    <div style="font-size:20px;">
        Budget et plateformes d'achat
    </div>
    """,
    unsafe_allow_html=True
)




col1, col2 = st.columns([3, 8])

with col1:
    df["budget_mensuel"] = df["budget_mensuel"].str.replace(r"\s*\(.*?\)", "", regex=True)

    st.plotly_chart(generic_bar(df, "budget_mensuel", title="Répartition des budgets mensuels",legend_title = {"x": "Budget mensuel", "y": "Nombre de votes"}), use_container_width=True)
with col2:
    st.plotly_chart(generic_multi_bar(df, "plateformes_achat", sep=",",legend_title = {"x": "Platrformes d'achats", "y": "Nombre de votes"}, title="Quelles sont les plateformes d'achats les plus utilisées ?", protected_groups=["Magasins traditionnels (Leclerc, King Jouet, Amazon, ...)","Boutiques Spécialisées (Cartabaffe, Coin des barons, FujiStore, Pikaplasma, ...)","Seconde Main en ligne (Vinted, Ebay, LeBonCoin, FB Marketplace, ...)","Plateformes d'enchères (Voggt, Whatnot, Shiny live, ...)","Brocantes","Salons TCG - Conventions"]))




st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Les ouvertures
    </div>
    """,
    unsafe_allow_html=True
)

coly, colz, col2456 = st.columns([1, 1, 1])

with coly:
    st.plotly_chart(generic_pie(df, "boosters_par_mois",title="Nombre de boosters ouverts par mois"), use_container_width=True)
with colz:
    st.plotly_chart(generic_multi_bar(df, "rapport_ouverture", sep=",", horizontal=False, title="Votre rapport à l'ouverture",legend_title = {"x": "Rapport à l'ouverture", "y": "Nombre de votes"}), use_container_width=True)
with col2456:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Les graphiques montrent que la majorité des collectionneurs ouvrent peu de boosters chaque mois — <b> la plupart entre 0 et 5</b>  —, signe d’une ouverture modérée et maîtrisée.<br><br>
        Le rapport à l’ouverture reste <b>avant tout lié au plaisir et à la passion</b>, plus qu’à la recherche du profit ou du “hit”.<br><br> 
        On observe cependant une part non négligeable de collectionneurs qui jugent les <b>ouvertures trop coûteuses</b>, illustrant la montée des prix sur le marché Pokémon.

    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)





st.markdown("---") 
st.markdown(
    """
    <div style="font-size:20px;">
        L'investissement
    </div>
    """,
    unsafe_allow_html=True
)
col499, col999 = st.columns([3, 5])

with col499:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        <b>Définition du mot "investisseur" : </b> Qui réalise des investissements.<br><br>
        <b>Définition du mot "investissement" : </b>Décision par laquelle un individu, une entreprise ou une collectivité <b>affecte ses ressources propres</b> ou des fonds empruntés <b>à l'accroissement de son stock de biens productifs</b>.
    </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)
with col999:
    st.plotly_chart(generic_pie(df, "investisseur", title="Vous considérez-vous comme des investisseurs ?"), use_container_width=True)


col2099, col2199 = st.columns([1,1])
with col2099:
    st.plotly_chart(generic_bar(df, "valeur_investissements", title="Quelle est la valeur de votre investissement ?",legend_title = {"x": "Valeur investissement", "y": "Nombre de votes"}), use_container_width=True)

with col2199:
   st.plotly_chart(generic_multi_bar(df, "investissements_type", sep=",", horizontal=True,legend_title = {"x": "Nombre de votes", "y": "Type d'investissement"},title="Type d'investissement"), use_container_width=True)


col2499, col2599 = st.columns([3,8])
with col2499:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        L'avis qui ressort le plus concernant l'investissement est un avis mitigé : <b>“Ok si c’est raisonné et pas du scalping.”.</b><br><br>
        Ensuite quasiment à égalité on retrouve le positif et le négatif : “La spéculation est en train de tuer la collection.”, <b>“C’est le cancer du TCG.”</b>, “Ok si c’est raisonné et pas du scalping.”.<br><br>
        Au global nous avons donc <b>2 avis très contrastés</b> qui s'opposent.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with col2599:
    data = [
        ("Contre / Négatif", 28),
        ("Mitigé / Raisonné", 34),
        ("Positif / Opportunité financière", 25),
        ("Nécessaire / Inévitable", 22),
        ("Passion avant l’argent", 21),
        ("Sans avis / NSP", 10)
    ]

    dfx = pd.DataFrame(data, columns=["avis", "votes"])

    fig = px.bar(
        dfx,
        x="avis",
        y="votes",
        text="votes",
        title="Avis sur l'investissement dans Pokémon (140 répondants)",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Catégories d'opinion",
        yaxis_title="Nombre de réponses",
        title_font_size=22,
        xaxis_tickangle=-20
    )
    st.plotly_chart(fig, use_container_width=True)






st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Plateforme d'enchères
    </div>
    """,
    unsafe_allow_html=True
)


col4, col9 = st.columns([1, 2])

with col4:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Je me demandais encore si ces plateformes étaient encore à la mode en France, étant donné que j'ai arrêté de les fréquenter il y a maintenant plusieurs années.
        <br><br>Il faut notifier sur ce graphe que 34 votants ont votés à la fois pour <b>Whatnot et pour Voggt</b> en même temps, proportionnellement les utilisateurs de ce type de plateformes ne représentent donc que <b>27% des sondés</b>.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)
with col9:
    st.plotly_chart(generic_multi_pie(df, "plateformes_encheres", title="Utilisez-vous ces plateformes ?", sep=","))




col6, col7, col8 = st.columns([1, 1, 1])

with col6:
    st.plotly_chart(generic_bar(df, "avis_enchere_prix", title="Votre avis sur les prix",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col7:
    st.plotly_chart(generic_bar(df, "avis_enchere_ambiance", title="Votre avis sur l'ambiance",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col8:
    st.plotly_chart(generic_bar(df, "avis_enchere_formats", title="Votre avis sur les formats",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)





col10, col11, col111 = st.columns([1, 1,1])
with col10:
    st.plotly_chart(generic_bar(df, "avis_enchere_produits", title="Votre avis sur les produits",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col11:
    st.plotly_chart(generic_bar(df, "avis_enchere_petitslives", title="Votre avis sur les petits lives",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col111:
    st.plotly_chart(generic_bar(df, "avis_enchere_eventlives", title="Votre avis sur les lives évênements",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)



commentaire = """
<div style="font-size:20px; line-height:1.6;">
    <br>
    Ces graphiques et les retours d’expérience mettent en évidence un <b>désamour global envers les plateformes d’enchères Pokémon</b>.<br>
    Bien que <b>27 % des répondants</b> les utilisent, la majorité déclare ne pas s’y intéresser ou avoir cessé d’y participer, jugeant ces espaces <b>trop axés sur le profit</b> et éloignés de la passion de la collection.<br><br>
    Les avis sur les <b>prix</b> sont majoritairement négatifs : les utilisateurs estiment que les produits sont <b>trop chers</b>, qu’il y a une **forte spéculation** et que certaines pratiques commerciales <b>frôlent la manipulation</b>.<br><br> 
    Côté <b>ambiance</b>, les retours sont plus nuancés — certains apprécient les échanges sur les petits lives, mais dénoncent le <b>climat malsain et toxique</b> des gros streams.<br>
    Les <b>formats et produits</b> sont jugés répétitifs ou peu authentiques, et beaucoup regrettent que ces plateformes soient devenues des “<b>pompes à fric</b>” dominées par des vendeurs opportunistes.<br><br> 
    Plusieurs témoignages soulignent également la <b>perte de contrôle sur les dépenses</b> (“on peut vite exploser le budget sans s’en rendre compte”) et la <b>dégradation du concept</b> (“c’était génial il y a deux ans, maintenant c’est gangrené”).<br><br>
    En somme, si ces plateformes peuvent encore <b>permettre de bonnes affaires sur les petits lives</b>, elles sont aujourd’hui perçues comme <b>symptomatiques de la dérive spéculative du marché Pokémon</b>, au détriment de l’esprit communautaire et de la passion initiale.
    </div>
"""
st.markdown(commentaire, unsafe_allow_html=True)

df_counts2 = clean_and_count_column(df, "avis_plateformes_general") 





st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Les boutiques Pokémon
    </div>
    """,
    unsafe_allow_html=True
)

col1000, col1100, col11100 = st.columns([1, 1,1])
with col1000:
    st.plotly_chart(generic_bar(df, "avis_boutique_prix",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, title="Votre avis sur les prix", ordered_colors=True), use_container_width=True)
with col1100:
    st.plotly_chart(generic_bar(df, "avis_boutique_fiabilite",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, title="Votre avis sur la fiabilité des boutiques", ordered_colors=True), use_container_width=True)
with col11100:
    st.plotly_chart(generic_bar(df, "avis_boutique_dispo",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, title="Votre avis sur la dispo des produits", ordered_colors=True), use_container_width=True)


col2400, col2500 = st.columns([3,8])
with col2400:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Quelle est votre boutique préférée ?
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

df_counts2 = clean_and_count_column(df, "boutique_preferee") 

with col2500:
    #plt = wordcloud_plot(df_counts2, column="word", title="mots les plus cités")
    #st.pyplot(plt)
    pass




st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Les conventions
    </div>
    """,
    unsafe_allow_html=True
)

col4, col9 = st.columns([1, 2])

with col4:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Globalement <b>les conventions font l'unanimité</b>, la plupart d'entre nous y sont allés ou aimeraient y aller prochainement.
        Les votes le montrent, leur importance a été relevée.<br>
        Le peuple sont plutôt<b> satisfait des prix d'entrée</b>, de la <b>qualité des exposants</b> ainsi que de la disponibilités des produits.<br><br>
        Les défauts majeurs qui sont revenus par contre sont les<b> tarifs exercés sur place ainsi que la sécurité</b> au sein de l'évènement.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with col9:
    st.plotly_chart(generic_pie(df, "convention_tcg",title="Vous-êtes vous déjà rendu en convention ?"), use_container_width=True)

col10001, col11001, col111001 = st.columns([1, 1,1])
with col10001:
    st.plotly_chart(generic_bar(df, "avis_convention_prix", title="Votre avis sur les prix d'entrée",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col11001:
    st.plotly_chart(generic_bar(df, "avis_convention_exposants", title="Votre avis sur les exposants",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col111001:
    st.plotly_chart(generic_bar(df, "avis_convention_importance", title="Votre avis sur leur importance",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)

col10002, col11002, col111002 = st.columns([1, 1,1])
with col10002:
    st.plotly_chart(generic_bar(df, "avis_convention_dispo", title="Votre avis sur les disponibilités",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col11002:
    st.plotly_chart(generic_bar(df, "avis_convention_tarifs", title="Votre avis sur les tarifs",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with col111002:
    st.plotly_chart(generic_bar(df, "avis_convention_securite", title="Votre avis sur la sécurité",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)

commentaire = """
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    En résumé, ces conventions sont des <b>évènements incontournables pour la communauté</b>, mais ils sont à qualité inégale.<br>
    Sans les citer, 2 des trois évènements majeurs sont salués, tandis qu'un autre est de plus en plus critiqué.<br><br>
    Les autres défauts qui ont été soulignés sont le <b>manque d'espaces d'échanges</b>, des zones mal gérées ainsi que des vols facilités par le désordre.<br>
    Ce qui est au contraire le plus apprécié c'est le fait de <b>mettre des visages sur les pseudos</b> et l'échange en général.    
    </div>
"""
st.markdown(commentaire, unsafe_allow_html=True)



st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Arnaque et Sécurité
    </div>
    """,
    unsafe_allow_html=True
)

col2400999, col2500999 = st.columns([3,8])
with col2400999:
    st.plotly_chart(generic_pie(df, "arnaque", title="Avez-vous subi des arnaques ?"), use_container_width=True)

with col2500999:
    st.plotly_chart(generic_multi_bar(df, "type_arnaque", sep=",", title="Quelles arnaques ?",legend_title = {"x": "Nombre de votes", "y": "Types d'arnaques"}), use_container_width=True)



col987, col9876 = st.columns([3,8])
with col987:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        <b>Une majorité des collectionneurs ont donc subi une arnaque</b>, on constate des problèmes avec les achats et ventes à distance, via des abus de confiance, des états qui diffèrent ou des colis vides.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with col9876:
    st.plotly_chart(generic_multi_bar(df, "service_securite", sep=",", horizontal=True, top_n=5, title="Ou laissez-vous votre collection ?",legend_title = {"x": "Nombre de votes", "y": "Lieu de stockage"}), use_container_width=True)


st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Les réseaux sociaux
    </div>
    """,
    unsafe_allow_html=True
)

colll, colllll,colipo = st.columns([1,1,1])
with colll:
    st.plotly_chart(generic_multi_bar(df, "echanges", sep=",", title="Avez-vous déjà réalisé des échanges ?",legend_title = {"x": "Nombre de votes", "y": "Types d'échanges"},protected_groups=["Oui - en main propre lors de bourses d'échange, conventions, ...","Oui - en main propre hors bourses","Oui - à distance","Non - mais j'aimerai","Brocantes","Non -  cela ne m'intéresse pas"]), use_container_width=True)

with colllll:
    st.plotly_chart(generic_multi_bar(df, "reseaux_sociaux", sep=",", title="Les réseaux sociaux privilégiés",legend_title = {"x": "Nombre de votes", "y": "Réseaux sociaux"}), use_container_width=True)
with colipo:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br><br>
        Les réseaux sociaux privilégiés par les collectionneurs sont de très loin <b>Instagram et Discord</b>. Juste derrière on retrouve Facebook, qui nous montre un tournant dans la communauté Pokémon, les groupes Facebook étant en quelque sorte "démodés".
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)





st.markdown("---") 

st.markdown(
    """
    <div style="font-size:20px;">
        Le contenu et l'influence
    </div>
    """,
    unsafe_allow_html=True
)

col98755, col987655 = st.columns([3,8])
with col98755:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Lorsqu'on parle de différents formats sur YouTube, je suis obligé de préciser que mon contenu tourne autour de la présentation de classeurs, évidemment <b>léger biais</b> au niveau des réponses.<br><br>
        On constate que Les formats favoris de la communauté Pokémon sont <b>......</b>.<br><br>
        Il faut noter que les nouveaux formats tournés en réel semblent prendre de plus en plus de place comme les<b> Vlogs en brocantes ou alors les vendeurs POV</b> qui ont été citées plusieurs fois alors que ce n'était pas une de mes propositions.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)
with col987655:
    st.plotly_chart(generic_bar(df, "contenu_youtube_prefere", title="Contenu favoris",legend_title = {"x": "Nombre de votes", "y": "Type de contenus"}), use_container_width=True)
    pass

cola, colb, colc = st.columns([1,1,1])
with cola:
    st.plotly_chart(generic_bar(df, "avis_youtube_qualite", title="Votre avis sur la qualité",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with colb:
    st.plotly_chart(generic_bar(df, "avis_youtube_diversite", title="Votre avis sur la diversité",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)
with colc:
    st.plotly_chart(generic_bar(df, "avis_youtube_redondance", title="Votre avis sur la redondance",legend_title = {"x": "Nombre de votes", "y": "Les votes"}, ordered_colors=True), use_container_width=True)


commentaire = """
<div style="font-size:20px; line-height:1.6;">
    <br><br>
    Le YouTube Pokémon français est perçu comme <b>globalement qualitatif</b> (90 votes sur 140 le jugent “plutôt bon”), mais souffre d’un <b>manque de diversité</b> et d’une <b>forte redondance des formats</b>.<br>
    Les contenus tournent souvent autour des ouvertures de boosters, de la <b>course aux hits</b> et des <b>thématiques d’investissement</b>, ce qui lasse une partie du public. <br>
    Beaucoup regrettent le <b>manque d’authenticité</b> et la surenchère dans les titres et réactions, parlant même d’une “DavidLafargisation” du paysage YouTube Pokémon. <br><br>
    Les spectateurs réclament davantage de <b>contenus artistiques, humains et instructifs</b>, mettant en avant les illustrateurs, les collections personnelles et les rencontres entre passionnés. <br><br>
    En résumé, même si la qualité reste bonne, la <b>diversité est limitée</b> (62 “plutôt bon” contre 35 “plutôt mauvais”) et la <b>lassitude s’installe</b>, avec 50 personnes jugeant la redondance “plutôt mauvaise”, 27 “très mauvaise” et 51 seulement “plutôt bonne”.
    </div>
"""
st.markdown(commentaire, unsafe_allow_html=True)


colf,coline, colg = st.columns([1,1,1])
with colf:
    st.plotly_chart(generic_pie(df, "plateforme_video_preferee",title="Plateforme préférée"), use_container_width=True)
with coline:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        La plateforme préférée pour regarder du contenu est aujourd'hui <b>YouTube, juste devant Instagram</b> tout de même loin derrière.<br><br>
        Pour ce qui concerne le format les contenus long semblent encore être les plus appréciés, très loin devant les formats verticaux.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with colg:
    st.plotly_chart(generic_pie(df, "format_video_prefere",title="Longueur du contenu privilégiée"), use_container_width=True)

colh, coli = st.columns([1,1])
with colh:
    commentaire = """
    <div style="font-size:20px; line-height:1.6;">
        <br><br>
        Pour finir, un des sondages qui m'a le plus surpris, la proportion de personnes <b>qui fais déjà du contenu sur un réseau social arrive en seconde position</b>, juste devant les personnes qui souhaitent en faire.<br><br>
        Cela montre bien à quel point la communauté est investie dans ce hobby qu'est Pokémon.
        </div>
    """
    st.markdown(commentaire, unsafe_allow_html=True)

with coli:
    st.plotly_chart(generic_pie(df, "envie_creation_contenu", title="Avez-vous envie de créer du contenu sur les réseaux sociaux ?"), use_container_width=True)
