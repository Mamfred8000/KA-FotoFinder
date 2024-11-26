import streamlit as st
import src.database
import src.utils

def get_photo_param():
    query_params = st.query_params
    if 'photo_id' in query_params:
        photo_id = query_params['photo_id']
    else:
        photo_id = 'nA'
    return photo_id

def init_startValues():
    st.session_state.device_mode = src.utils.set_deviceMode()
    st.session_state.init_flag = True
    st.session_state.user_name = ""
    st.session_state.marker_pos = [49.01357217893837, 8.404385447502138]
    st.session_state.zoom = 13
    st.session_state.guess_position = [0, 0]
    st.session_state.photo_id = get_photo_param()
    st.session_state.photo_position = src.database.query_photo_position()

# MAIN
def main():
    st.title("KA-FotoFinder")
    st.write("Das Ziel des Spiels ist, den Aufnahmeort des Fotos möglichst genau zu erraten.")
    st.write("Dafür den QR-Code auf dem Foto scannen und dann auf der Karte den potenitellen Ort anklicken.")
    st.write("Viel Spaß! Grüße, Moritz")
    if st.session_state.user_name:
        st.write("Viel Spaß beim raten!")
        if st.button("Starten", type="primary"): st.switch_page("pages/1_quiz.py")
    else:
        st.write("### Wie heißt du?")
        name = st.text_input("Wie heißt du?", placeholder="Name")
        if name:
            st.session_state.user_name = name
            st.rerun()

if __name__ == "__main__":
    if 'init_flag' in st.session_state:
        main()
    else:
        src.database.init_db()
        init_startValues()
        st.rerun()

# Output für Entwicklung
#st.write(st.session_state)