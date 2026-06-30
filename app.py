import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

st.set_page_config(page_title="IMDb Dashboard", layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('imdb_top_1000_cleaned.csv')
    return df
df = load_data()

@st.cache_resource
def get_connection():
    conn = sqlite3.connect('imdb.db', check_same_thread=False)
    df = load_data()
    df.to_sql('movies', conn, if_exists='replace', index=False)
    return conn
conn = get_connection()

st.sidebar.title("Filters")
min_rating = st.sidebar.slider("Minimum IMDb Rating", 7.0, 9.3, 7.0)
all_genres = sorted(set(
    g.strip()
    for genres in df['Genre'].dropna()
    for g in genres.split(', ')
))
selected_genre = st.sidebar.selectbox('Genre', ['All'] + all_genres)

filtered = df[df['IMDB_Rating'] >= min_rating]
if selected_genre != 'All':
    filtered = filtered[filtered['Genre'].str.contains(selected_genre, na=False)]

st.title("IMDb Top 1000 -- Analytics Dashboard")
st.write(f"Showing **{len(filtered)}** movies with rating >= {min_rating}"
         + (f" in genre **{selected_genre}**" if selected_genre != 'All' else ""))

st.divider()
if filtered.empty:
        st.warning('No movies matches these filters. Try adjusting the filters')
        st.stop()
col1, col2 = st.columns(2)

with col1:
    st.subheader("***Rating Distribution***")
    sns.set_theme(style='darkgrid')
    fig, ax=plt.subplots(figsize=(6, 4))
    sns.histplot(data=filtered, x='IMDB_Rating', bins=20, color='mediumseagreen', edgecolor='black', kde=True, ax=ax)
    ax.set_xlabel('IMDb_Rating')
    ax.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader('***Avg Rating by Genre (Top 8)***')
    df_genres = filtered.assign(Genre=filtered['Genre'].str.split(', ')).explode('Genre')
    top_genres = df_genres['Genre'].value_counts().head(8).index
    df_top = df_genres[df_genres['Genre'].isin(top_genres)]
    genre_order= (df_top.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False).index)
    sns.set_theme(style='darkgrid')
    fig, ax=plt.subplots(figsize=(6, 4))
    if df_top.empty:
        st.warning('No data for current filters')
    else:
        bars = sns.barplot(data=df_top, x='Genre', y='IMDB_Rating', hue='Genre', palette='viridis', legend=False, order=genre_order, ax=ax)
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, fontsize=9)
        ax.set_xlabel('Genre')
        ax.set_ylabel('Avg Rating')
        ax.tick_params(axis='x', rotation=30)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader('***Correlation Heatmap***')
    numeric_cols = filtered[['IMDB_Rating', 'Meta_score', 'No_of_Votes', 'Gross', 'Runtime']].dropna()
    if len(numeric_cols) < 2:
        st.warning('Not enough data to compute correlation with current filters.')
    else:
        corr_matrix = numeric_cols.corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, linewidths=0.5, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

with col4:
    st.subheader('***Movies Per Decade***')
    temp = filtered.copy()
    temp['Decade'] = (temp['Released_Year'] // 10) * 10
    decade_counts = temp.groupby('Decade')['Series_Title'].count()
    sns.set_theme(style='darkgrid')
    fig, ax=plt.subplots(figsize=(6, 4))
    ax.plot(decade_counts.index, decade_counts.values, color='cyan', linewidth=2.5, marker='o', markersize=7)
    ax.set_xlabel('Decade')
    ax.set_ylabel('Number of Movies')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader('***SQL Query Explorer***')
st.caption('Table name: movies -- write any SELECT query below')

default_query = """
SELECT Director, COUNT(*) as movie_count, ROUND(AVG(IMDB_Rating), 2) as avg_rating
FROM movies
GROUP BY Director
HAVING movie_count >= 3
ORDER BY avg_rating DESC 
"""

query = st.text_area('SQL Query', value=default_query, height=120)
if st.button('Run Query'):
    try:
        result = pd.read_sql_query(query, conn)
        st.success(f'{len(result)} rows returned')
        st.dataframe(result)
    except Exception as e:
        st.error(f"SQL Error: {e}")

st.divider()
if st.checkbox('Show raw filtered data'):
    st.caption(f'{len(filtered)} rows x {len(filtered.columns)} columns')