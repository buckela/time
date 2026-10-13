import time
import streamlit as st
import re 

def en_minutes(horaire):
    heures, minutes = map(int, horaire.split(":"))
    return heures * 60 + minutes

st.set_page_config(page_title="Time", page_icon="⌛")

parse_input = st.text_input("Parsing")

miditmp_input = None
st.text("Prévision format : 00:00")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    arr_input = st.text_input("Heure d'arrivé")
    if arr_input and en_minutes(arr_input) > en_minutes("08:30"):
        st.text("Erreur, horaire de début max: 8h30")
    if arr_input and en_minutes(arr_input) < en_minutes("07:45"):
        st.text("Erreur, horaire de début min: 7h45")

with c2:
    if not miditmp_input:
        midi1_input = st.text_input("Heure début midi")
        if midi1_input and en_minutes(midi1_input) < en_minutes("11:45"):
            st.text("Erreur, horaire de début min: 11h45")
        if midi1_input and en_minutes(midi1_input) > en_minutes("11:45"):
            st.text("Erreur, horaire de début max: 12h45")

with c3:
    if not miditmp_input:
        midi2_input = st.text_input("Heure de fin midi")
        if midi2_input and en_minutes(midi2_input) > en_minutes("13:30"):
            st.text("Erreur, horaire de fin max: 13h30")
        if midi2_input and en_minutes(midi2_input) > en_minutes("12:30"):
            st.text("Erreur, horaire de fin min: 12h30")

with c4:
    if not (midi1_input or midi2_input):
        miditmp_input = st.text_input("Temps de pause midi")
        if miditmp_input and en_minutes(miditmp_input) > en_minutes("01:45"):
            st.text("Erreur, temps de pause max : 1h45")
        if miditmp_input and en_minutes(miditmp_input) < en_minutes("00:45"):
            st.text("Erreur, temps de pause min : 0h45")

with c5:
    fin_input = st.text_input("Heure de fin ")
    if fin_input and en_minutes(fin_input) < en_minutes("16:15"):
        st.text("Erreur, heure de fin min : 16h15")
    if fin_input and en_minutes(fin_input) > en_minutes("17:30"):
        st.text("Erreur, heure de fin max : 17h30")

parsed = re.findall(r'\b\d{2}:\d{2}\b', parse_input)

st.text(f"parsed:\n{parsed}")


result = 90
size = len(parsed)
if size>=2:
    result -= en_minutes("08:30")-en_minutes(parsed[0])
if size>=6:
    diff = max(en_minutes(parsed[4])-en_minutes(parsed[2]),45)
    result -= (105-diff)

fin = en_minutes("16:15") + result
heure_fin = fin // 60
minutes_fin = fin % 60

st.text(f"Temps restant hors nominal: {result} minutes.\n Fin à {heure_fin}:{minutes_fin}.")
