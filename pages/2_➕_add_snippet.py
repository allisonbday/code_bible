import streamlit as st
import sqlite3
import os
from datetime import datetime


# PAGE SET UP -----------------------------------------------------------------

st.set_page_config(
    page_icon="📖",
    page_title="Allison's Code Bible",
    # page_icon=":material/cognition:",
    # layout="wide",
    menu_items={
        # "Get Help": "",
        # 'Report a bug': "",
    },
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


# PAGE CONTENT ----------------------------------------------------------------
icon("➕")
st.title("Add a New Snippet")

# Add a new snippet
# st.header("Add a New Snippet")

title = st.text_input("Title")
description = st.text_area("Caption / Description")
project = st.selectbox(
    "Project", options=["Code Bible", "Work", "Color Contrast Tester"], index=None
)

c1, c2 = st.columns([0.3, 0.7])

with c1:
    language = st.selectbox(
        "Language",
        options=[
            "python",
            "sql",
            "r",
            "java",
            "scala",
            "julia",
            "rust",
            "bash",
            "git",
            "javascript",
            "css",
            "mermaid",
        ],
        index=0,
        help="[language list 🔗](https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD)",
    )

with c2:
    tags = st.pills(
        "Tags",
        options=[
            "pandas",
            "steamlit",
            "web-scraping",
            "APIs",
            "jupyter",
            "vscode",
            "git",
            "matplotlib",
            "seaborn",
            "plotly",
            "statsmodels",
            "data-cleaning",
            "data-wrangling",
            "data-visualization",
            "etl",
            "data-pipelines",
            "sql",
            "spark",
            "azure",
            "windows",
            "quarto",
            # "classification",
            # "regression",
            # "hyperparameter-tuning",
            # "neural-networks",
            # "sentiment-analysis",
            # "scipy",
            # "scikit-learn",
            # "tensorflow",
            # "keras",
            # "pytorch",
            # "nosql",
            # "mongodb",
            # "postgresql",
            # "mysql",
            # "sqlite",
            # "hadoop",
            # "dask",
            # "hive",
            # "pig",
            # "clustering",
            # "dimensionality-reduction",
            # "model-evaluation",
            # "cnn",
            # "rnn",
            # "lstm",
            # "gan",
            # "autoencoders",
            # "nlp",
            # "text-mining",
            # "topic-modeling",
            # "word-embeddings",
            # "docker",
            # "airflow",
            # "mlflow",
            # "aws",
            # "gcp",
            # "bigquery",
            # "redshift",
            # "s3",
        ],
        selection_mode="multi",
    )


tab1, tab2 = st.tabs(["Write Code", "Display Code"])

with tab1:
    code = st.text_area(
        "Code",
    )

with tab2:
    # Custom CSS to change the font size of st.code
    st.markdown(
        """
        <style>
        .stCodeBlock {
            font-size: 50px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.code(code, language=language, wrap_lines=True)


notes = st.text_area("Notes")


# Database connection and table creation
conn = sqlite3.connect("src/data/snippets.db")
c = conn.cursor()

# Add project column if it doesn't exist
c.execute("PRAGMA table_info(snippets)")
columns = [col[1] for col in c.fetchall()]
if "project" not in columns:
    c.execute("ALTER TABLE snippets ADD COLUMN project TEXT")

c.execute(
    """
    CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        project TEXT,
        language TEXT,
        tags TEXT,
        code TEXT,
        notes TEXT,
        created_at TIMESTAMP
    )
"""
)

# Insert snippet into database
if st.button("Save Snippet"):
    created_at = datetime.now()
    c.execute(
        """
        INSERT INTO snippets (title, description, project, language, tags, code, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            title,
            description,
            project,
            language,
            ",".join(tags),
            code,
            notes,
            created_at,
        ),
    )
    conn.commit()
    st.success("Snippet saved successfully!")

conn.close()
