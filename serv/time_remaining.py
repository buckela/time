import time
import streamlit as st

st.set_page_config(page_title="Time", page_icon="🚢")


parse_input = st.text_input("parsing")

parsed = parse_input

st.text(f"parsed:\n{parsed}")

