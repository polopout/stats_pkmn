import streamlit as st
from PIL import Image
from utils.viz import sidebar_logo

st.set_page_config(page_title="Questionnaire Pokémon", layout="wide")

st.title("Review et Analyse des résultats du questionnaire")

sidebar_logo()

commentaire = """
<div style="
    text-align: center; 
    font-size: 25px; 
    border: 2px solid black; 
    border-radius: 15px; 
    padding: 20px; 
    margin: 30px 0;
">
    <br>
    Cette analyse a été menée à la fois par <b>curiosité personnelle</b> et en lien direct avec mon métier de <b>data analyst</b>.<br><br>
    Je suis <b>Polopout</b>, collectionneur passionné et créateur de contenu sur YouTube, où je partage régulièrement des <b>réceptions de cartes</b> ainsi que le <b>rangement de ma collection en classeur</b>.<br><br>
    Il est important de noter qu’il existe un <b>biais de participation</b> : une partie des répondants provient de ma communauté et peut donc être davantage orientée vers ce type de pratiques.<br><br>
    Le sondage compte actuellement <b>137 participants</b>, ce qui constitue une base intéressante mais encore limitée.<br><br>
    Je vous invite donc à continuer de répondre : si un nombre significatif de nouvelles personnes participe, je pourrai proposer une <b>mise à jour enrichie</b> de cette analyse.<br>
    <a href="https://forms.gle/UcTC18Ty16C1eUiq5" target="_blank">Répondre au sondage ici</a>
</div>
"""

st.markdown(commentaire, unsafe_allow_html=True)

