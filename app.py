import time
import streamlit as st
from streamlit_javascript import st_javascript
import streamlit.components.v1 as components

def init_deviceMode():
    user_agent = st_javascript("window.navigator.userAgent")
    #Javascript library has loading time
    timeout = 60  # seconds
    start_time = time.time()
    while True:
        if isinstance(user_agent, str):
            st.session_state.device_mode = "mobile" if "Mobi" in user_agent else "desktop"
            break
        elif time.time() - start_time > timeout:
            st.write("Timeout feching javascript data reached; exiting loop.")
            break
        else:
            time.sleep(0.01)

# Query Parameter lesen
def get_photo_param():
    query_params = st.query_params
    if 'photo_id' in query_params:
        photo_id = query_params['photo_id']
    else:
        photo_id = 'nA'
    return photo_id

def get_photo_position():
    pos = [48.99511114804374, 8.402958512306215]
    return pos

def read_photo_position():
    df = st.session_state.conn.query('SELECT * FROM "photo-list";')
    if st.session_state.photo_id in df['photo_id'].values:
        lat = df.loc[df['photo_id'] == st.session_state.photo_id, 'latitude'].values[0]
        long = df.loc[df['photo_id'] == st.session_state.photo_id, 'longitude'].values[0]
    else:
        [lat, long] = [0, 0]
    return [lat, long]

def init():
    st.session_state.init_flag = True
    st.session_state.user_name = ""
    st.session_state.marker_pos = [49.01357217893837, 8.404385447502138]
    st.session_state.zoom = 13
    st.session_state.guess_position = [0, 0]
    st.session_state.photo_id = get_photo_param()
    st.session_state.photo_position = read_photo_position()

def init_database():
    st.session_state.conn = st.connection("postgresql", type="sql")

def DEAC_query():
    query = 'SELECT * FROM "KAFotoFinder-Scoreboard" WHERE device_id = :device_id;'
    df = st.session_state.conn.query(
        query,
        ttl=5,
        params = {"device_id" : st.session_state.device_id}
        )

# Hauptfunktion
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
        init_deviceMode()
        init_database()
        init()
        st.rerun()

# Output für Entwicklung
st.write(st.session_state)