# IMDb Top 1000 — Analytics Dashboard

An interactive Streamlit dashboard analyzing the IMDb Top 1000 movies dataset — built as Level 3 of my Data Science & AI/ML roadmap, covering data visualization (Matplotlib, Seaborn) and SQL (SQLite).

## 🚀 Live Demo
[View the dashboard](https://your-app-url.streamlit.app)

## Features
- Interactive filters — minimum rating slider, genre dropdown
- Rating distribution histogram (Seaborn)
- Average rating by genre, sorted with value labels (Seaborn)
- Correlation heatmap of numeric features (Seaborn)
- Movies released per decade (Matplotlib)
- Live SQL query explorer against the dataset (SQLite)
- Raw data viewer

## Tech Stack
Python · Pandas · Matplotlib · Seaborn · SQLite · Streamlit

## Project Structure
- `app.py` — the dashboard
- `notebooks/` — exploration notebooks from learning each library (Matplotlib, Seaborn, SQL)
- `imdb_top_1000_cleaned.csv` — cleaned dataset (cleaned in an earlier EDA project)

## Run Locally
\`\`\`bash
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Related Project
This dashboard reuses the dataset cleaned in [imdb-eda](https://github.com/revanthraghava08/imdb-eda), my Level 2 EDA project.