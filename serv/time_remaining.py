""" Page pour calculer les horaires variables chez NG"""

import time
import streamlit as st
import re 

# Fonction pour transformer le format 00:00 en minutes int
def en_minutes(horaire):
    # format XX:YY, on split -> (XX, YY)
    try:
        heures, minutes = map(int, horaire.split(":"))
    except:
        try:
            heures, minutes = horaire.split("h")
            heures = int(heures)
            minutes = int(minutes) if minutes else 0
        except:
            try:
                heures, minutes = horaire.split(".")
                heures = int(heures)
                minutes = int(minutes) if minutes else 0
            except:
                try:
                    heures = int(horaire)
                    minutes = 0
                except:
                    st.text("format accepté : 00:00 ou 00h00 ou 0.00")
    finally:
        # Calcul XX * 60 + YY
        return heures * 60 + minutes


def en_heure(minutes):
    return f"{minutes//60}:{minutes % 60}"


def htomadd(a, b):
    return en_minutes(a) + en_minutes(b)


def hadd(a, b):
    res = htomadd(a, b)
    return en_heure(res)


def htomsous(a, b):
    return en_minutes(a) - en_minutes(b)


def hsous(a, b):
    res = htomsous(a, b)
    return en_heure(res)


TMP_TRAVAIL = en_minutes("07:30")
HEURE_EWEN = "12:00"
MINUTE_EWEN = en_minutes(HEURE_EWEN)

# Setup le streamlit avec le titre et l'icone
st.set_page_config(page_title="Time", page_icon="⌛")

# Demande d'entrer le copier coller
parse_input = st.text_input("Parsing")

# Regex pour extraire les dates
parsed = re.findall(r'\b\d{2}:\d{2}\b', parse_input)

# Affiche les données parsées pour vérifié qu'elles sont bonnes
# st.text(f"parsed:{parsed}")


# Fonction qui calcul et affiche le temps restant
def afficher_restant(parsed):
    # Temps minimal théorique à faire par jour en minutes ( en dehors du temps obligatoire )
    result = 90
    # On récupère le nombre d'élément
    size = len(parsed)
    # En fonction du nombre d'élément, alors on décompte le temps supplémentaire
    if size > 0:
        # Matin avant 8h30
        result -= htomsous("08:30", parsed[0])
    if size > 2:
        # Aprem au 3ème badgage
        diff = max(htomsous(parsed[2], parsed[1]), 45)
        result -= (105-diff)
    # Affichage
    st.text(f"Temps restant hors nominal: {result} minutes.\n Fin à {hadd("16:15", en_heure(result))}.")


# Si il y a des données entrées dans le 1er input, alors on calcul et affiche
if parsed and len(parsed) > 0:
    parsed3 = [parsed[0]]
    if len(parsed) > 2:
        parsed3.append(parsed[2])
        if len(parsed) > 4:
            parsed3.append(parsed[4])
    afficher_restant(parsed3)

# Pour chaque champ prévisionnel, on vérifie que l'input est bon
miditmp_input = None
# st.text("Prévision format : 0:0 , 0h0 , 0.0")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    arr_input = st.text_input("Heure d'arrivé")
    if arr_input and en_minutes(arr_input) > en_minutes("08:30"):
        st.text("Erreur, horaire de début max: 8h30")
    if arr_input and en_minutes(arr_input) < en_minutes("07:45"):
        st.text("Erreur, horaire de début min: 7h45")

with c2:
    midi1_input = st.text_input("Heure début midi")
    if midi1_input and en_minutes(midi1_input) < en_minutes("11:45"):
        st.text("Erreur, horaire de début min: 11h45")
    if midi1_input and en_minutes(midi1_input) > en_minutes("12:45"):
        st.text("Erreur, horaire de début max: 12h45")

with c3:
    midi2_input = st.text_input("Heure de fin midi")
    if midi2_input and en_minutes(midi2_input) > en_minutes("13:30"):
        st.text("Erreur, horaire de fin max: 13h30")
    if midi2_input and en_minutes(midi2_input) < en_minutes("12:30"):
        st.text("Erreur, horaire de fin min: 12h30")

with c4:
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


def print_tmp_pause_midi(début, fin):
    pause = htomsous(fin, début) - TMP_TRAVAIL
    if pause < 45:
        st.text("Impossible pause trop courte")
    else:
        st.text(f"Nombre de minutes possible à midi : {pause} minutes.\n à choisir entre 11h45 et 13h30.")
        if st.button("Ewen"):
            tmp_fin_midi_ewen = MINUTE_EWEN + pause
            if tmp_fin_midi_ewen > 13 * 60 + 30:
                st.text(f"Trop de temps de pause : {pause}, tu peux finir plus tôt Ewen.\nHeure de fin de midi théorique: {en_heure(tmp_fin_midi_ewen)}")
            else:
                st.text(f"Ewen tu doit commencer la pause à {HEURE_EWEN}, et la finir à {en_heure(tmp_fin_midi_ewen)}")


def option_combinatoire(debut, fin, tmp_midi, midi1, midi2):
    if debut and tmp_midi:
        if midi1:
            if htomadd(midi1, tmp_midi) > en_minutes("13:30"):
                st.text(f"Erreur : Début trop tard ou pause midi trop longue : fin {hadd(tmp_midi, midi1)}")
            else:
                parsed3 = [debut, midi1, hadd(tmp_midi, midi1)]
                afficher_restant(parsed3)
        elif midi2:
            if htomsous(midi2, tmp_midi) < en_minutes("11h45"):
                st.text(f"Erreur : Fin trop tôt ou pause trop longue : début {hsous(midi2, tmp_midi)}")
            else:
                parsed3 = [debut, midi1, hsous(midi2, tmp_midi)]
                afficher_restant(parsed3)
        else:
            var_time = 90
            var_time -= htomsous("8h30", debut)
            var_time -= htomsous("1h45", tmp_midi)
            st.text(f"Temps restant:{var_time}. Fin à {hadd("16h15", en_heure(var_time))}")

    elif debut and midi1 and midi2:
        parsed3 = [debut, midi1, midi2]
        afficher_restant(parsed3)
    else:
        if debut and fin:
            print_tmp_pause_midi(debut, fin)


# Calcul du temps de pause possible à midi en fonction du début et fin de journée
if not parsed:
    option_combinatoire(arr_input, fin_input, miditmp_input, midi1_input, midi2_input)
else:
    if arr_input:
        option_combinatoire(arr_input, fin_input, miditmp_input, midi1_input, midi2_input)
    elif parsed[0]:
        option_combinatoire(parsed[0], fin_input, miditmp_input, midi1_input, midi2_input)
