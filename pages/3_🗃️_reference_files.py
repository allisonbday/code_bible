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


def add_border(txt, radius=0.5):
    return f"<span style='line-height: 1px;padding: .5rem; border: 1px solid rgba(49, 51, 63, 0.2);border-radius: {radius}rem;'>{txt}</span>"


def clean_projects(project):
    if project == None:
        return ""
    else:
        return project


# PAGE CONTENT ----------------------------------------------------------------
icon("🗃️")
st.title("Reference Files")

# Add a new snippet
# st.header("Reference Files")
