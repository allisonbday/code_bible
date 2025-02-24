import streamlit as st
import sqlite3
import os


# Streamlit app
st.title("Code Bible")

# Add a new snippet
st.header("Add a New Snippet")
title = st.text_input("Title")
code = st.text_area("Code")
description = st.text_area("Description")
