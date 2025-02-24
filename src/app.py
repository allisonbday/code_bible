import streamlit as st
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/snippets.db')
c = conn.cursor()

# Function to fetch snippets from the database
def fetch_snippets():
    c.execute("SELECT * FROM snippets")
    return c.fetchall()

# Function to add a new snippet to the database
def add_snippet(title, code):
    c.execute("INSERT INTO snippets (title, code) VALUES (?, ?)", (title, code))
    conn.commit()

# Streamlit app layout
st.title("Favorite Code Snippets")

# Sidebar for adding new snippets
st.sidebar.header("Add a New Snippet")
snippet_title = st.sidebar.text_input("Snippet Title")
snippet_code = st.sidebar.text_area("Snippet Code")
if st.sidebar.button("Add Snippet"):
    add_snippet(snippet_title, snippet_code)
    st.sidebar.success("Snippet added!")

# Displaying snippets
st.header("Code Snippets")
snippets = fetch_snippets()
for snippet in snippets:
    st.subheader(snippet[1])  # Title
    st.code(snippet[2])  # Code

# Close the database connection
conn.close()