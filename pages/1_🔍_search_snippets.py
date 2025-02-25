import streamlit as st
import sqlite3
import os
from datetime import datetime


# PAGE SET UP -----------------------------------------------------------------

st.set_page_config(
    page_icon="📖",
    page_title="Allison's Code Bible",
    # icon=":material/sports_motorsports:",
    # layout="wide",
    menu_items={
        # "Get Help": "",
        # 'Report a bug': "",
        "About": "This app allows you to simulate the F1 season with a custom points system.",
    },
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


# FUNCTIONS -------------------------------------------------------------------


def mdy_to_ymd(d):
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d")


def fancy_markdown(
    txt,
    radius=0.5,
    color=None,
    background_color=None,
    border_size=1,
    border_color=None,
    font_size=None,
    text_align="left",
    font_style="normal",
):
    return f"<span style='font-style: {font_style}; font-size: {font_size}px; text-align: {text_align}; line-height: 1px;padding: .5rem; border: {border_size}px solid {border_color};border-radius: {radius}rem;color: {color};background-color: {background_color};'>{txt}</span>"


def clean_projects(project):
    if project == None:
        return ""
    else:
        return project


# PAGE CONTENT ----------------------------------------------------------------
icon("🔍")
st.title("Search Snippets")

# Add a new snippet
# st.header("Search Snippets")

c1, c2 = st.columns(2)

with c1:
    search_query = st.text_input("Enter search query")

with c2:
    language_query = st.selectbox(
        "Select language",
        [
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
        # placeholder="any",
        index=None,
    )


tag_query = st.pills(
    "Select tags",
    [
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
    ],  # Replace with actual tags
    selection_mode="multi",
)

# Database connection
conn = sqlite3.connect("src/data/snippets.db")
c = conn.cursor()


def search_snippets(query, language, tags):
    if not query and not language and not tags:
        c.execute("SELECT * FROM snippets ORDER BY created_at DESC")
    else:
        tag_filter = " OR ".join([f"tags LIKE '%{tag}%'" for tag in tags])
        if not language:
            if tags:
                c.execute(
                    f"SELECT * FROM snippets WHERE (title LIKE ? OR description LIKE ? OR code LIKE ?) AND ({tag_filter}) ORDER BY created_at DESC",
                    (f"%{query}%", f"%{query}%", f"%{query}%"),
                )
            else:
                c.execute(
                    "SELECT * FROM snippets WHERE title LIKE ? OR description LIKE ? OR code LIKE ? ORDER BY created_at DESC",
                    (f"%{query}%", f"%{query}%", f"%{query}%"),
                )
        else:
            if tags:
                c.execute(
                    f"SELECT * FROM snippets WHERE (title LIKE ? OR description LIKE ? OR code LIKE ?) AND language = ? AND ({tag_filter}) ORDER BY created_at DESC",
                    (f"%{query}%", f"%{query}%", f"%{query}%", language),
                )
            else:
                c.execute(
                    "SELECT * FROM snippets WHERE (title LIKE ? OR description LIKE ? OR code LIKE ?) AND language = ? ORDER BY created_at DESC",
                    (f"%{query}%", f"%{query}%", f"%{query}%", language),
                )
    return c.fetchall()


def snippet_disp(snippet):
    with st.container():

        c1, c2 = st.columns([0.8, 0.2])

        with c1:
            st.subheader(snippet[1])  # Title
            if snippet[2]:
                st.caption(snippet[2])  # Description

        with c2:
            # st.caption(f"*{mdy_to_ymd(snippet[7])}*")  # Created
            st.markdown(
                fancy_markdown(
                    mdy_to_ymd(snippet[7]),
                    font_size=14,
                    color="#727272",
                    font_style="italic",
                    border_color=None,
                    border_size=0,
                    text_align="right",
                ),
                unsafe_allow_html=True,
            )

        if snippet[8]:  # Project
            with c2:
                st.markdown(
                    fancy_markdown(
                        clean_projects(snippet[8]),
                        color="#727272",
                        border_color="#727272",
                        font_size=10,
                        text_align="right",
                    ),
                    unsafe_allow_html=True,
                )

        if snippet[4]:  # Tags
            # st.pills(
            #     f"Tags",
            #     options=snippet[4]snippet[4],
            #     disabled=True,
            #     key=snippet[0],
            #     label_visibility="hidden",
            # )

            tags = snippet[4].split(",")

            tag_txt = ""
            for tag in tags:
                tag_txt += (
                    fancy_markdown(
                        f"{tag}",
                        radius=1,
                        color="red",
                        border_color="red",
                        font_size=12,
                    )
                    + " "
                )
            st.markdown(
                f"{tag_txt}",
                unsafe_allow_html=True,
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"Language: `{snippet[3]}`")  # Language

        st.code(snippet[5], language=snippet[3], wrap_lines=True)  # Code

        if snippet[6]:  # Notes
            st.markdown(
                f"""##### Notes
                        
{snippet[6]}"""
            )  # Notes

        st.write("---")


if search_query or language_query or tag_query:
    snippets = search_snippets(search_query, language_query, tag_query)
    if snippets:
        st.write("---")
        for snippet in snippets:
            snippet_disp(snippet)
    else:
        st.write("No snippets found.")
else:
    snippets = search_snippets("", "", [])
    st.write("---")
    for snippet in snippets:
        snippet_disp(snippet)

# Close the database connection
conn.close()
