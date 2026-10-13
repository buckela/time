""" Page pour calculer les horaires variables chez NG"""

import time
import streamlit as st
import re 

# Fonction pour transformer le format 00:00 en minutes int
def en_minutes(horaire):
    # format XX:YY, on split -> (XX, YY)
    heures, minutes = map(int, horaire.split(":"))
    # Calcul XX * 60 + YY
    return heures * 60 + minutes

# Setup le streamlit avec le titre et l'icone
st.set_page_config(page_title="Time", page_icon="⌛")

# Demande d'entrer le copier coller
parse_input = st.text_input("Parsing")

# Regex pour extraire les dates
parsed = re.findall(r'\b\d{2}:\d{2}\b', parse_input)

# Affiche les données parsées pour vérifié qu'elles sont bonnes
st.text(f"parsed:{parsed}")

# Fonction qui calcul et affiche le temps restant
def afficher_restant(parsed):
    # Temps minimal théorique à faire par jour en minutes ( en dehors du temps obligatoire )
    result = 90
    # On récupère le nombre d'élément
    size = len(parsed)
    # En fonction du nombre d'élément, alors on décompte le temps supplémentaire
    if size > 0:
        # Matin avant 8h30
        result -= en_minutes("08:30")-en_minutes(parsed[0])
    if size > 2:
        # Aprem au 3ème badgage 
        diff = max(en_minutes(parsed[2])-en_minutes(parsed[1]),45)
        result -= (105-diff)

    # Calcul de l'heure de fin
    fin = en_minutes("16:15") + result
    # Formatage de l'heure de fin pour l'afficher
    heure_fin = fin // 60
    minutes_fin = fin % 60
    # Affichage
    st.text(f"Temps restant hors nominal: {result} minutes.\n Fin à {heure_fin}:{minutes_fin}.")

# Si il y a des données entrées dans le 1er input, alors on calcul et affiche
if parsed:
    parsed3 = [parsed[0], parsed[2], parsed[4]]
    afficher_restant(parsed3)

# Pour chaque champ prévisionnel, on vérifie que l'input est bon
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
        if midi1_input and en_minutes(midi1_input) > en_minutes("12:45"):
            st.text("Erreur, horaire de début max: 12h45")

with c3:
    if not miditmp_input:
        midi2_input = st.text_input("Heure de fin midi")
        if midi2_input and en_minutes(midi2_input) > en_minutes("13:30"):
            st.text("Erreur, horaire de fin max: 13h30")
        if midi2_input and en_minutes(midi2_input) < en_minutes("12:30"):
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


# En fonction des combinaison d'input, on affichera des résultats 
if arr_input and midi1_input and midi2_input:
    parsed3 = [arr_input, midi1_input, midi2_input]
    afficher_restant(parsed3)