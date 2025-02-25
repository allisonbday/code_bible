import streamlit as st

# PAGE SET UP -----------------------------------------------------------------

st.set_page_config(
    page_icon="📖",
    page_title="Allison's Code Bible",
    # icon=":material/sports_motorsports:",
    layout="wide",
    menu_items={
        # "Get Help": "",
        # 'Report a bug': "",
        "About": "A second brain and second home to all of my coding snippets, so I can stop hoarding and have truly ✨clean✨ code",
    },
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


# PAGE CONTENT ----------------------------------------------------------------
icon("📖")
st.title("Code Bible")


st.caption(
    f"""A second brain and second home to all of my coding snippets, so I can stop hoarding and have truly ✨clean✨ code"""
)


st.header("Welcome to Allison's Code Bible!")
st.write(
    """
    This app is designed to help me, Allison, store, search, and manage all my coding snippets efficiently. 
    """
)
