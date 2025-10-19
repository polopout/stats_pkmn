import folium
from streamlit_folium import st_folium
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import streamlit as st
import pandas as pd

# ----- Carte des départements -----
def plot_dept_map(gdf, dept_counts):
    # Fusion
    gdf_plot = gdf.merge(dept_counts, on="departement", how="left")
    gdf_plot["count"] = gdf_plot["count"].fillna(0)

    # Carte Folium
    m = folium.Map(location=[46.5, 2], zoom_start=6, tiles="CartoDB positron")
    folium.Choropleth(
        geo_data=gdf_plot,
        name="choropleth",
        data=gdf_plot,
        columns=["departement", "count"],
        key_on="feature.properties.departement",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Nombre de réponses"
    ).add_to(m)

    # Popups
    for _, row in gdf_plot.iterrows():
        if row["count"] > 0:
            folium.Marker(
                location=[row["geometry"].centroid.y, row["geometry"].centroid.x],
                popup=f"{row['nom']} : {int(row['count'])} réponses"
            ).add_to(m)

    return m


def wordcloud_plot(df_counts, column="word", title="Nuage de mots"):
    """Nuage de mots à partir d'un DataFrame avec colonnes 'word' et 'count'"""
    word_freq = dict(zip(df_counts[column], df_counts["count"]))
    wc = WordCloud(width=800, height=400, background_color="white", colormap="magma").generate_from_frequencies(word_freq)
    
    # Plot avec matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    
    return plt


def generic_pie(df, column, title=None, title_font_size=24):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "count"]

    if title is None:
        title = f"Répartition par {column}"

    fig = px.pie(
        counts,
        names=column,
        values="count",
        title=title
    )

    # Personnaliser la taille du titre
    fig.update_layout(title_font_size=title_font_size)

    return fig



def generic_bar(
    df, 
    column, 
    title=None, 
    top_n=None, 
    horizontal=False, 
    title_font_size=24, 
    legend_title=None, 
    ordered_colors=False
):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "count"]

    if top_n:
        counts = counts.head(top_n)

    if title is None:
        title = f"Répartition par {column}"

    # Définir les labels
    if legend_title is None:
        labels = {column: column, "count": "Nombre"}
    else:
        if horizontal:
            labels = {"count": legend_title.get("x", "Nombre"), column: legend_title.get("y", column)}
        else:
            labels = {column: legend_title.get("x", column), "count": legend_title.get("y", "Nombre")}

    # Si on veut forcer ordre + couleurs
    color_args = {}
    if ordered_colors:
        ordered_categories = ["Très mauvais", "Plutôt mauvais", "Plutôt bon", "Très bon"]
        colors = {
            "Très mauvais": "red",
            "Plutôt mauvais": "orange",
            "Plutôt bon": "blue",
            "Très bon": "green"
        }

        counts[column] = pd.Categorical(counts[column], categories=ordered_categories, ordered=True)
        counts = counts.sort_values(by=column)
        color_args = {"color": column, "color_discrete_map": colors}

    # Plot
    if horizontal:
        fig = px.bar(
            counts,
            x="count",
            y=column,
            orientation="h",
            text="count",
            title=title,
            labels=labels,
            **color_args
        )
    else:
        fig = px.bar(
            counts,
            x=column,
            y="count",
            text="count",
            title=title,
            labels=labels,
            **color_args
        )

    fig.update_traces(textposition="outside")
    fig.update_layout(title_font_size=title_font_size)
    return fig


def _split_outside_parentheses(s, sep=','):
    """Split s on sep but ignore sep inside parentheses. sep should be a single char."""
    parts = []
    cur = []
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            if depth > 0:
                depth -= 1
        if ch == sep and depth == 0:
            token = ''.join(cur).strip()
            if token:
                parts.append(token)
            cur = []
        else:
            cur.append(ch)
    last = ''.join(cur).strip()
    if last:
        parts.append(last)
    return parts

def generic_multi_bar(df, column, sep=",", horizontal=False, title=None,
                      protected_groups=None, top_n=None, title_font_size=24, legend_title=None):
    """
    Crée un bar chart générique avec possibilité de protéger certains regroupements
    et de limiter aux top_n éléments.

    - sep: caractère séparateur (ex: ",")
    - protected_groups: liste de chaînes complètes à préserver (peuvent contenir des virgules dans des parenthèses)
    - legend_title: dict optionnel {"x": "Nom X", "y": "Nom Y"}
    """
    if protected_groups is None:
        protected_groups = []

    all_items = []

    for raw_val in df[column].dropna():
        val = str(raw_val).strip()

        # enlever guillemets parasites autour de la cellule
        val = val.strip('"').strip("'").strip()

        # Remplacer temporairement chaque groupe protégé par un placeholder unique
        placeholders = {}
        temp = val
        for i, pg in enumerate(protected_groups):
            if pg and pg in temp:
                ph = f"__PG_{i}__"
                temp = temp.replace(pg, ph)
                placeholders[ph] = pg

        # Splitter uniquement sur les sep au niveau 0 (autour des parenthèses)
        parts = _split_outside_parentheses(temp, sep=sep)

        # Remettre les placeholders par leur texte d'origine et nettoyer chaque token
        cleaned_parts = []
        for p in parts:
            p = p.strip()
            # remettre placeholder -> groupe protégé si nécessaire
            if p in placeholders:
                token = placeholders[p]
            else:
                token = p
            # nettoyage léger : enlever guillemets internes, trim
            token = token.replace('"', '').replace("'", "").strip()
            if token:
                cleaned_parts.append(token)

        all_items.extend(cleaned_parts)

    # Compter les occurrences
    counter = Counter(all_items)
    counts_df = pd.DataFrame({
        column: list(counter.keys()),
        "count": list(counter.values())
    }).sort_values(by="count", ascending=False).reset_index(drop=True)

    # Limiter au top_n si demandé
    if top_n is not None:
        counts_df = counts_df.head(top_n)

    if title is None:
        title = f"Répartition par {column}"

    # labels dynamiques selon legend_title et orientation
    if legend_title is None:
        labels = {column: column, "count": "Nombre"}
    else:
        if horizontal:
            labels = {"count": legend_title.get("x", "Nombre"), column: legend_title.get("y", column)}
        else:
            labels = {column: legend_title.get("x", column), "count": legend_title.get("y", "Nombre")}

    # Plot
    if horizontal:
        fig = px.bar(counts_df, x="count", y=column, orientation="h", text="count", title=title, labels=labels)
    else:
        fig = px.bar(counts_df, x=column, y="count", text="count", title=title, labels=labels)

    fig.update_traces(textposition="outside")
    fig.update_layout(title_font_size=title_font_size)
    return fig




def _split_outside_parentheses(s, sep=','):
    """Split s on sep but ignore sep inside parentheses. sep doit être un seul caractère."""
    parts = []
    cur = []
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            if depth > 0:
                depth -= 1
        if ch == sep and depth == 0:
            token = ''.join(cur).strip()
            if token:
                parts.append(token)
            cur = []
        else:
            cur.append(ch)
    last = ''.join(cur).strip()
    if last:
        parts.append(last)
    return parts

def generic_multi_pie(df, column, sep=",", title=None, protected_groups=None, title_font_size=24):
    """
    Crée un pie chart générique avec possibilité de protéger certains regroupements.

    Args:
        df: DataFrame
        column: nom de la colonne à analyser
        sep: séparateur par défaut
        title: titre du graphique
        protected_groups: liste de chaînes exactes qu’on ne doit pas splitter
                         (ex: ["Du récent (EV, EB)", "Du semi-vintage (SL, XY, NB)"])
    """
    if protected_groups is None:
        protected_groups = []

    all_items = []

    for raw_val in df[column].dropna():
        val = str(raw_val).strip()
        val = val.strip('"').strip("'").strip()

        # Remplacer les groupes protégés par placeholders
        placeholders = {}
        temp = val
        for i, pg in enumerate(protected_groups):
            if pg and pg in temp:
                ph = f"__PG_{i}__"
                temp = temp.replace(pg, ph)
                placeholders[ph] = pg

        # Split en ignorant les virgules dans les parenthèses
        parts = _split_outside_parentheses(temp, sep=sep)

        # Restaurer placeholders et nettoyer
        for p in parts:
            p = p.strip()
            if p in placeholders:
                token = placeholders[p]
            else:
                token = p
            token = token.replace('"', '').replace("'", "").strip()
            if token:
                all_items.append(token)

    # Compter les occurrences
    counter = Counter(all_items)
    counts_df = pd.DataFrame({
        column: list(counter.keys()),
        "count": list(counter.values())
    }).sort_values(by="count", ascending=False)

    if title is None:
        title = f"Répartition par {column}"

    # Plot pie chart
    fig = px.pie(
        counts_df,
        names=column,
        values="count",
        title=title,
        hole=0.3  # donut style (enlève si tu veux un pie classique)
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title_font_size=title_font_size)
    return fig





def sidebar_logo():
    st.sidebar.image("data\\pub2.png", use_container_width=True)  
